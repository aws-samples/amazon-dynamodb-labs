#!/bin/bash

GUID=$1
WORKSHOP_ZIP="$2"
AWS_REGION=$3
AWS_ACCOUNT_ID=$4
DDB_REPLICATION_ROLE="$5"
CFN_WAIT_HANDLE="$6"

function log
{
  NANOSEC=`date +%N`
  echo -e [`date -u +"%Y-%m-%dT%H:%M:%S"`.${NANOSEC:0:3}Z] "$@"
}
function is_baked
{
  if [[ -f /etc/designpatterns/baking_manifest/$1 ]]; then
    true
  else
    false
  fi
}
function mark_installed
{
    mkdir -p /etc/designpatterns/baking_manifest/
    echo `date -u` > /etc/designpatterns/baking_manifest/$1-manifest
}
function sync_clock
{
  log Synchronizing network time in background.
  nohup sh -c "service ntpd stop; ntpdate -u 0.amazon.pool.ntp.org 1.amazon.pool.ntp.org 2.amazon.pool.ntp.org 3.amazon.pool.ntp.org; service ntpd start" &
}


function update_mirror_list
{
  for i in updates preview gpu nosrc hvm graphics; do
    local repo_file="/etc/yum.repos.d/amzn-$i.repo"
    if [ -f $repo_file ]; then
      sed -i -r 's/mirror.list$/mirror.list-$guid/' $repo_file
    fi

    local template_file="/etc/cloud/templates/amzn-$i.repo.tmpl"
    if [ -f $template_file ]; then
      sed -i -r 's/mirror.list$/mirror.list-\\$guid/' $template_file
    fi
  done
}



function lock_repo_version
{
  if is_baked lock_repo_version_${GUID}-manifest; then
    log yum repo has already been locked to $GUID.
  else
    log Locking yum repo version to GUID.
    mkdir -p /etc/yum/vars
    echo $GUID > /etc/yum/vars/guid
    chmod 644 /etc/yum/vars/guid

    update_mirror_list

    yum clean -y all || echo Warning: cannot clean local yum cache. Continue...
    mark_installed lock_repo_version_$GUID
    log Completed yum repo version locking.
  fi
}

function update_yum_packages
{
  if is_baked update_yum_packages_${GUID}-manifest; then
    log yum update has already been done.
  else
    log Updating yum packages.
    yum --exclude=aws-cfn-bootstrap update -y || echo Warning: cannot update yum packages. Continue...
    mark_installed update_yum_packages_$GUID

    # Update system-release RPM package will reset the .repo files
    # Update the mirror list again after yum update
    update_mirror_list

    log Completed updating yum packages.
  fi
}

function pull_workshop_zip
{
  mkdir -p /home/ec2-user/workshop
  chown -R ec2-user:ec2-user /home/ec2-user/workshop
  curl -o /home/ec2-user/workshop/workshop.zip  -O "${WORKSHOP_ZIP}"
  unzip -o /home/ec2-user/workshop/workshop.zip -d /home/ec2-user/workshop
  sed -i -- "s/region/${AWS_REGION}/g" /home/ec2-user/workshop/iam-role-policy.json
  sed -i -- "s/accountID/${AWS_ACCOUNT_ID}/g" /home/ec2-user/workshop/iam-role-policy.json
  echo ${DDB_REPLICATION_ROLE} > /home/ec2-user/workshop/ddb-replication-role-arn.txt
  rm /home/ec2-user/workshop/workshop.zip
  chown -R ec2-user:ec2-user /home/ec2-user/workshop/*
}

function configure_aws_cli
{
  mkdir -p /home/ec2-user/.aws
  chown -R ec2-user:ec2-user /home/ec2-user/.aws
  cat > /home/ec2-user/.aws/config <<EOF
[default]
region = ${AWS_REGION}
output = json
EOF
}

function configure_python_and_install
{
  log Installing Python3.6
  yum install -y python36
  alternatives --set python /usr/bin/python3.6

  log Installing workshop requirements.
  /usr/bin/pip-3.6 install -r /home/ec2-user/workshop/requirements.txt

  log frustrating pip user installs
  mkdir /home/ec2-user/.local 1>&2 2>/dev/null
  chattr +i /home/ec2-user/.local

}
function verify_configuration_and_signal
{
  log verify_configuration_and_signal running.
  log Checking if python36 installed by yum.
  yum list installed python36 1>/dev/null || signal_failure_and_exit "Python3.6 not installed correctly."

  log Checking if python scripts are in workshop directory.
  ls -l /home/ec2-user/workshop/*.py 1>/dev/null || signal_failure_and_exit "Python scripts not in workshop directory."

  signal_success
}
function lock_instance
{
  cat > /etc/profile.d/motd.sh << "EOF"
  cat <<"ENDOFFILE"
                           ,---.
                          /    |
                         /     |
 You shall not pass!    /      |
                       /       |
          \       ___,'        |
                <  -'          :
                 `-.__..--'``-,_\_
                    |o/ <o>` :,.)_`>
                    :/ `     ||/)
                    (_.).__,-` |\
                    /( `.``   `| :
                    \'`-.)  `  ; ;
                    | `       /-<
                    |     `  /   `.
    ,-_-..____     /|  `    :__..-'\
   /,'-.__\\  ``-./ :`      ;       \
   `\ `\  `\\  \ :  (   `  /  ,   `. \
     \` \   \\   |  | `   :  :     .\ \
      \ `\_  ))  :  ;     |  |      ): :
     (`-.-'\ ||  |\ \   ` ;  ;       | |
      \-_   `;;._   ( `  /  /_       | |
       `-.-.// ,'`-._\__/_,'         ; |
          \:: :     /     `     ,   /  |
           || |    (        ,' /   /   |
           ||                ,'   /    |
*****************************************
***       Error:                      ***
***       This EC2 instance is not    ***
***       bootstrapped yet. Exiting.  ***
***       Return later.               ***
*****************************************
ENDOFFILE
logout
EOF
}

function unlock_instance
{
  rm -f /etc/profile.d/motd.sh 1>2 2>/dev/null
}
function signal_success
{
  /opt/aws/bin/cfn-signal --success true $CFN_WAIT_HANDLE
}
function signal_failure_and_exit
{
  /opt/aws/bin/cfn-signal --success false $CFN_WAIT_HANDLE --reason "$@"
  log failure signal sent to CloudFormation: "${@}"
  exit 0
}

#Main Execution
lock_instance
sync_clock

pull_workshop_zip
configure_aws_cli

lock_repo_version
update_yum_packages

configure_python_and_install
verify_configuration_and_signal
unlock_instance
