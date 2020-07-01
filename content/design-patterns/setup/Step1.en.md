+++
title = "Step 1 - Open the AWS Systems Manager Console "
date = 2019-12-02T10:07:45-08:00
weight = 10
#TODO mod-xxx is not the same name when running in EC2
+++



1. Once you've gained access to the AWS Management Console for the lab, double check the region is correct and the TeamRole is selected.
1. In the services search bar, search for Systems Manager and click on it to open the AWS Systems Manager section of the AWS Management Console.
1. In the AWS Systems Manager console, select Session Manager on the left side.
1. Choose "Start session" to launch a shell session.
1. Click the radio button to select the EC2 instance for the lab. If you see no instance, wait a few minutes and then click refresh. Wait until the ec2 instance beginning with name 'mod-xxxx...' is available before continuing.
1. Select start session.
1. In the new black shell, switch to the ec2-user account by running ```sudo su - ec2-user```
    ```bash
    sudo su - ec2-user
    ```
1. run ```shopt login_shell``` and be sure it says ```login_shell     on```. Then, change into the workshop directory to begin: ```cd ~/workshop```
   ```bash
   #Verify login_shell is 'on'
   shopt login_shell
   #Change into the workshop directory
   cd ~/workshop
   ```

The output of your commands in the Session Manager session should look like the following:
```bash
sh-4.2$ sudo su - ec2-user
[ec2-user@ip-172-31-24-0 ~]$ #Verify login_shell is 'on'
[ec2-user@ip-172-31-24-0 ~]$ shopt login_shell
login_shell     on
[ec2-user@ip-172-31-24-0 ~]$ #Change into the workshop directory
[ec2-user@ip-172-31-24-0 ~]$ cd ~/workshop
```
