---
title: "Scheduled Backup"
menuTitle: "Scheduled Backup"
date: 2020-04-21T07:38:58-05:00
weight: 64
---


You must create at least one vault before creating a backup plan or
starting a backup job.

1.  In the AWS Management Console, navigate to **Services -&gt; AWS
    Backup.** Click on **Create Backup vault** under **Backup vaults**.

:image[Scheduled Backup 1]{src="/static/images/hands-on-labs/backup/sched_backup_1.png" disableZoom=true width=950}


2.  Provide Backup vault name of your choice. AWS KMS encryption master
    key. By default, AWS Backup creates a master key with the alias
    aws/backup for you. You can choose that key or choose any other key
    in your account. Click on **Create Backup vault**.

:image[Scheduled Backup 2]{src="/static/images/hands-on-labs/backup/sched_backup_2.png" disableZoom=true width=650}

After a few moments, you will see the Backup vault has been created successfully.

:image[Scheduled Backup 3]{src="/static/images/hands-on-labs/backup/sched_backup_3.png" disableZoom=true width=650}

Now, we need to create backup plan.

3.  Click on **Create Backup plan** under **Backup plans**.

:image[Scheduled Backup 4]{src="/static/images/hands-on-labs/backup/sched_backup_4.png" disableZoom=true width=950}

4.  Select **Build a new plan**. Provide **backup plan name** and **rule
    name**.

:image[Scheduled Backup 5]{src="/static/images/hands-on-labs/backup/sched_backup_5.png" disableZoom=true width=650}

5.  Select the **backup vault** we created earlier. Next, select **backup frequency.** The backup frequency determines how
    often a backup is created. Using the console, you can choose a
    **frequency** of every 12 hours, daily, weekly, or monthly. Choose a
    **backup window**. The backup window consists of the time when the
    backup begins and the duration of the window in hours. Backup
    jobs are started within this window. Here, we are configuring the backup to start within 1 hour of 18:00 UTC and to complete within 4 hours.

:image[Scheduled Backup 6]{src="/static/images/hands-on-labs/backup/sched_backup_6.png" disableZoom=true width=650}

6. Select **Lifecycle**. The lifecycle defines when a backup is transitioned to cold storage and when it expires. Here, we are configuring the backup to move cold storage after 31 days and to expire after 365 days.

:image[Scheduled Backup 7]{src="/static/images/hands-on-labs/backup/sched_backup_7.png" disableZoom=true width=650}

7.   At the bottom of the page, click on **Create plan**.

*Note: Backups that are transitioned to cold storage must be stored in
cold storage for a minimum of 90 days*

Next, assign the resource to backup plan. When you assign a resource to a
backup plan, that resource is backed up automatically according to the
backup plan.

8. Give Resource a assignment name. Choose the default role. Under "**1. Define resource selection**", select **Include specific resource types**.

:image[Scheduled Backup 8]{src="/static/images/hands-on-labs/backup/sched_backup_8.png" disableZoom=true width=650}

9.   Under "**2. Select specific resource types**", select the resource type **DynamoDB** in the dropdown. Click choose resources, uncheck **All Tables**, and select the **ProductCatalog** table. Click **Assign resources**.

:image[Scheduled Backup 9]{src="/static/images/hands-on-labs/backup/sched_backup_9.png" disableZoom=true width=650}

10.  You will only be able to see the status of your backup job under the jobs section after your scheduled backup window timeframe has passed. You will be able to see that your DynamoDB backup completed successfully.


### Restore a Backup

After a resource has been backed up at least once, it is considered
protected and is available to be restored using AWS Backup. A backup may not yet be available in your account. If this is the case, simply review the process below. 

1.  On the **Protected resources** page, you can explore details of the
    resources that are backed up in AWS Backup. Choose our DynamoDB
    table resource.

:image[Scheduled Backup 11]{src="/static/images/hands-on-labs/backup/sched_backup_11.png" disableZoom=true width=650}

2.  Choose the recovery point ID of the resource. Click on **Restore**. _Note: If you do not see a recovery point, you can click "Create an on-demand backup" and complete the backup. For the purposes of this lab, you need a completed backup to continue, and you may not want to wait for your backup plan's scheduled backup._

:image[Scheduled Backup 12]{src="/static/images/hands-on-labs/backup/sched_backup_12.png" disableZoom=true width=650}

3.  Provide new DynamoDB table name. Leave all the settings on the defaults and click
    **Restore backup**

:image[Scheduled Backup 13]{src="/static/images/hands-on-labs/backup/sched_backup_13.png" disableZoom=true width=650}

The **Restore jobs** pane appears. A message at the top of the page
provides information about the restore job. You can see job status is
running.After some time you can see status changes to completed


:image[Scheduled Backup 14]{src="/static/images/hands-on-labs/backup/sched_backup_14.png" disableZoom=true width=650}

You can also monitor the all backup and restore jobs in central
dashboard.

:image[Scheduled Backup 15]{src="/static/images/hands-on-labs/backup/sched_backup_15.png" disableZoom=true width=650}

To see the restored table,  go to the [DynamoDB Console](https://console.aws.amazon.com/dynamodbv2/) and click on *Tables* from the side menu.Choose
*ProductCatalogRestored* table. You can see the table is restored along with data.

:image[Scheduled Backup 16]{src="/static/images/hands-on-labs/backup/sched_backup_16.png" disableZoom=true width=650}