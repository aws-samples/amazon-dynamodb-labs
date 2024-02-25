#!/bin/bash
set -o xtrace

SCRIPT_VERSION=$1
AWS_ACCOUNT_ID=$2
AWS_REGION=$3
WorkshopZIP="$4" # ${WorkshopZIP}"
DDB_REPLICATION_ROLE="$5" #!Sub echo ${DDBReplicationRole.Arn} 

function log
{
  NANOSEC=`date +%N`
  echo -e "`date -u +"%Y-%m-%dT%H:%M:%S"`.${NANOSEC:0:3}" "$@"
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

function update_apt_packages
{
    log 'INSTALL and CONFIGURE default software components'
    . /home/ubuntu/.zshrc
    sudo apt-get update
    sudo apt-get -y install --ignore-missing sqlite telnet jq strace tree gcc python3 python3-pip gettext bash-completion awscli

}

function configure_cli_and_env
{
    if is_baked configure_cli_${SCRIPT_VERSION}-manifest; then
        log cli and env already configured
    else
        echo LANG=en_US.utf-8 >> /etc/environment
        echo LC_ALL=en_US.UTF-8 >> /etc/environment
        log CONFIGURE awscli and setting ENVIRONMENT VARS
        echo "complete -C '/usr/local/bin/aws_completer' aws" >> /home/ubuntu/.bashrc
        mkdir -p /home/ubuntu/.aws
        cat > /home/ubuntu/.aws/config <<EOF
[default]
region = ${AWS_REGION}
output = json
EOF
        #chmod 600 /home/ubuntu/.aws/config
        cat >> /home/ubuntu/.bashrc <<EOF
PATH=$PATH:/usr/local/bin'
export PATH' >> /home/ubuntu/.bashrc
EOF
        cat >> /home/ubuntu/.bash_profile <<EOF
export AWS_ACCOUNT_ID="${AWS_ACCOUNT_ID}" 
export AWS_REGION="${AWS_REGION}"
aws cloud9 update-environment --environment-id \$C9_PID --managed-credentials-action DISABLE --region $AWS_REGION &> /dev/null
rm -vf ${HOME}/.aws/credentials  &> /dev/null
EOF

        log CLEANING /home/ubuntu
        for f in cloud9; do rm -rf /home/ubuntu/$f; done
        chown -R ubuntu:ubuntu /home/ubuntu/
        mark_installed configure_cli_${SCRIPT_VERSION}
    fi
}

function setup_ladv
{
    log setting up LADV files
    rm -rf /home/ubuntu/workshop 1>&2 2>/dev/null
    mkdir -p /home/ubuntu/workshop
    chown -R ubuntu:ubuntu /home/ubuntu/workshop
    curl -o /home/ubuntu/workshop/workshop.zip "${WorkshopZIP}"
    unzip -o /home/ubuntu/workshop/workshop.zip -d /home/ubuntu/workshop
    echo ${DDB_REPLICATION_ROLE} > /home/ubuntu/workshop/ddb-replication-role-arn.txt
    rm /home/ubuntu/workshop/workshop.zip
    chown -R ubuntu:ubuntu /home/ubuntu/workshop/*
    sudo pip3 install boto3 opensearch-py > /dev/null 2>&1 
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
***       bootstrapped yet.  ***
***       Return later.               ***
*****************************************
ENDOFFILE
EOF
}
function unlock_instance
{
  rm -f /etc/profile.d/motd.sh 1>2 2>/dev/null
}
function end_and_reboot
{
    log PREPARE REBOOT in 1 minute
    sudo shutdown --reboot
    log Bootstrap completed with return code "${?}"
}

#Main Execution
lock_instance
update_apt_packages
configure_cli_and_env

setup_ladv
unlock_instance
end_and_reboot

