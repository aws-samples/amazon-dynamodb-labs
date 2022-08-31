+++
title = "Scheduled Backup"
menuTitle = "Scheduled Backup"
date = 2020-04-21T07:38:58-05:00
weight = 64
+++


You must create at least one vault before creating a backup plan or
starting a backup job.

1.  In the AWS Management Console, navigate to **Services -&gt; AWS
    Backup.** Click on **Create Backup vault** under **Backup vaults**.

![Scheduled Backup 1](/images/hands-on-labs/backup/sched_backup_1.png)

2.  Provide Backup vault name of your choice. AWS KMS encryption master
    key. By default, AWS Backup creates a master key with the alias
    aws/backup for you. You can choose that key or choose any other key
    in your account. Click on **Create Backup vault**

![Scheduled Backup 2](/images/hands-on-labs/backup/sched_backup_2.png)

You can see Backup vault is created successfully

![Scheduled Backup 3](/images/hands-on-labs/backup/sched_backup_3.png)

Now, we need to create backup plan.

3.  Click on **Create Backup plan** under **Backup plans**.

![Scheduled Backup 4](/images/hands-on-labs/backup/sched_backup_4.png)

4.  Select **Build a new plan**. Provide **backup plan name** and **rule
    name**.

![Scheduled Backup 5](/images/hands-on-labs/backup/sched_backup_5.png)

5.  Select **backup frequency.** The backup frequency determines how
    often a backup is created. Using the console, you can choose a
    **frequency** of every 12 hours, daily, weekly, or monthly. Choose a
    **backup window**. Backup window consists of the time that the
    backup window begins and the duration of the window in hours. Backup
    jobs are started within this window. I am configuring backup at 8 PM
    UTC start within 1 hour and completes within 4 hours.

	Further, select **lifecycle**. The lifecycle defines when a backup is
	transitioned to cold storage and when it expires. I am configuring
	backup to move cold storage after 31 days and expire after 366 days.

![Scheduled Backup 6](/images/hands-on-labs/backup/sched_backup_6.png)

*Note: Currently cold storage isn't supported for DynamoDB. Only Amazon
EFS file system backups can be transitioned to cold storage. However,
you should configure it anyway.*

6.  Select **backup vault** we created earlier. Click on **Create
    plan**.

![Scheduled Backup 7](/images/hands-on-labs/backup/sched_backup_7.png)

*Note: Backups that are transitioned to cold storage must be stored in
cold storage for a minimum of 90 days*

Now assign the resource to backup plan. When you assign a resource to a
backup plan, that resource is backed up automatically according to the
backup plan.

7.  Click on **Assign resources** under **Backup plans**.

![Scheduled Backup 8](/images/hands-on-labs/backup/sched_backup_8.png)

8.  Give Resource assignment name. Choose default IAM role. Choose our
    DynamoDB table in the assign resources section. Click on **Assign
    resources**.

![Scheduled Backup 9](/images/hands-on-labs/backup/sched_backup_9.png)

9.  You can see the status of your backup job under jobs section after
    your scheduled backup window timeframe. You can see your DynamoDB
    backup is completed.

![Scheduled Backup 10](/images/hands-on-labs/backup/sched_backup_10.png)

### Restore a Backup:

After a resource has been backed up at least once, it is considered
protected and is available to be restored using AWS Backup.

1.  On the **Protected resources** page, you can explore details of the
    resources that are backed up in AWS Backup. Choose our DynamoDB
    table resource.

![Scheduled Backup 11](/images/hands-on-labs/backup/sched_backup_11.png)

2.  Choose the recovery point ID of the resource. Click on **Restore**.

![Scheduled Backup 12](/images/hands-on-labs/backup/sched_backup_12.png)

3.  Provide new DynamoDB table name. Choose default role and click on
    **Restore backup**

![Scheduled Backup 13](/images/hands-on-labs/backup/sched_backup_13.png)

The **Restore jobs** pane appears. A message at the top of the page
provides information about the restore job. You can see job status is
running.After some time you can see status changes to completed

![Scheduled Backup 14](/images/hands-on-labs/backup/sched_backup_14.png)

You can also monitor the all backup and restore jobs in central
dashboard.

![Scheduled Backup 15](/images/hands-on-labs/backup/sched_backup_15.png)

To see the restored table,  go to the [DynamoDB Console](https://console.aws.amazon.com/dynamodbv2/) and click on *Tables* from the side menu.Choose
*ProductCatalogRestored* table. You can see the table is restored along with data.

![Scheduled Backup 16](/images/hands-on-labs/backup/sched_backup_16.png)
