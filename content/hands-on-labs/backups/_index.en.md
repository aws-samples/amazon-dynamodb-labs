+++
title = "Backups"
menuTitle = "Backups"
date = 2021-04-25T07:33:04-05:00
weight = 60
chapter = true
pre = "<b>6. </b>"

+++


[Amazon DynamoDB](https://aws.amazon.com/dynamodb/) offers two types of
backup,
[on-demand](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/BackupRestore.html)
and [point-in-time
recovery](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/PointInTimeRecovery.html)
(PITR). PITR is on a rolling window, on-demand backups stay around
forever (even after the table is deleted) until someone tells DynamoDB
to delete the backups. When you enable PITR, DynamoDB backs up your
table data automatically with per-second granularity. The retention
period is a fixed 35 days (5 calendar weeks) and can't be modified.
However, large enterprise customers who are used to deploying tradition
backup solutions in their data centers often want a centralized backup
solution that can schedule backups through “jobs” and handle tasks such
as expiring/deleting older backups time, monitoring the status of
on-going backups, verifying compliance, and finding / restoring backups,
all using a central console. At the same time they don't want to
manually manage their backups, create their own tools via scripts or
[AWS Lambda](https://aws.amazon.com/lambda/) functions, or use a
different solution for each application they have to protect. They want
the ability to have a standardized way to manage their backups at scale
to the resources in their AWS account.

[AWS Backup](https://aws.amazon.com/backup/) aims to be the single point
of centralize backup management and source of truth that customers can
rely on. You can schedule periodic or future backups by using AWS
Backup, The backup plans include schedules and retention policies for
your resources. AWS Backup creates the backups and deletes prior backups
based on your retention schedule. Backups of resources are always
required in case of disaster recovery.

AWS Backup removes the undifferentiated heavy lifting of manually making
and deleting On-demand backups by automating the schedule and deletion
for you. In this lab we will be exploring how to schedule periodic
backups of a DynamoDB table using AWS Backup. I am going to create a
backup plan where I take daily backup and keep it for a month. Next I
setup a backup rule to transition the backup to cold storage after 31
days and auto-delete the backup after 366 days from backup creation
date.

Also, I show you how you can restrict people in your organization to
delete the backups from AWS backup and DynamoDB console while able to do
others operations like create backup, create table etc.

Now lets dive into the different DynamoDB backup options.