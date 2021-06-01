+++
title = "Point-In-Time Recovery Backup"
menuTitle = "Point-In-Time Recovery Backup"
date = 2021-04-24T07:38:58-05:00
weight = 62
+++


[DynamoDB Point-in-time recovery](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/PointInTimeRecovery.html) aka **"PITR"** helps to protect your DynamoDB
tables from accidental write or delete operations. With point-in-time
recovery, you do not have to worry about creating, maintaining, or
scheduling on-demand backups. For example, suppose that a test script
writes accidentally to a production DynamoDB table. With point-in-time
recovery, you can restore that table to any point in time during the
last 35 days. DynamoDB maintains incremental backups of your table. By
default, PITR is disabled.

**<u>How to enable PITR</u>**

1.  First, go to the [DynamoDB Console](https://console.aws.amazon.com/dynamodbv2/) and click on *Tables* from the side menu.
In the list of tables, choose the ProductCatalog table.On the **Backups** tab of the ProductCatalog table in the  **Point-in-time recovery** section, choose **Edit**.

![PITR Backup 1](/images/hands-on-labs/backup/pitr_backup_1.png)

2.  Select **Enable Point-in-time-recovery** and choose **Save changes**.

![PITR Backup 2](/images/hands-on-labs/backup/pitr_backup_2.png)

**<u>To restore a table to a point in time</u>**

Now let us say we get some unwanted records in ProductCatalog table as highlighted below.

![PITR Unwanted Records](/images/hands-on-labs/backup/pitr_unwanted_records.png)

Follow the below steps to restore ProductCatalog using Point-in-time-recovery.

1.  Sign in to the AWS Management Console and open the DynamoDB console.
    In the navigation pane on the left side of the console, choose
    **Tables**. In the list of tables, choose the ProductCatalog table.
    On the **Backups** tab of the ProductCatalog table, in the
    **Point-in-time recovery** section, choose **Restore to
    point-in-time**.

![PITR Restore 1](/images/hands-on-labs/backup/pitr_restore_1.png)

2. For the new table name, enter ProductCatalogPITR. To confirm
the restorable time, set the **Restore date and time** to the **Latest
restore date**. Choose **Restore** to start the restore process.

![PITR Restore 2](/images/hands-on-labs/backup/pitr_restore_2.png)

*Note : You can restore the table to the same AWS Region or to a
different Region from where the backup resides. You can also exclude
secondary indexes from being created on the new restored table. In
addition, you can specify a different encryption mode.*

The table that is being restored is shown with the status **Restoring**.
After the restore process is finished, the status of the
*ProductCatalogPITR* table changes to **Active**.

![PITR Restore 3](/images/hands-on-labs/backup/pitr_restore_3.png)
