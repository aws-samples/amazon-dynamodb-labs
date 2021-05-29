+++
title = "Point-In-Time Recovery Backup"
menuTitle = "Point-In-Time Recovery Backup"
date = 2021-04-24T07:38:58-05:00
weight = 62
+++


DynamoDB Point-in-time recovery(PITR) helps to protect your DynamoDB
tables from accidental write or delete operations. With point-in-time
recovery, you do not have to worry about creating, maintaining, or
scheduling on-demand backups. For example, suppose that a test script
writes accidentally to a production DynamoDB table. With point-in-time
recovery, you can restore that table to any point in time during the
last 35 days. DynamoDB maintains incremental backups of your table. By
default, PITR is disabled.

**<u>How to enable PITR</u>**

1.  Sign in to the AWS Management Console and open the DynamoDB console.
    In the navigation pane on the left side of the console, choose
    **Tables**. In the list of tables, choose the ProductCatalog table.
    On the **Backups** tab of the ProductCatalog table, in the
    **Point-in-time recovery** section, choose **Edit**.

<img src="/images/hands-on-labs/backup/image1.png" />

2.  Select **Enable Point-in-time-recovery** and choose **Enable**

<img src="/images/hands-on-labs/backup/image2.png" />



**<u>To restore a table to a point in time</u>**

Now let us say we get some unwanted records in **ProductCatalog** table as highlighted below.

<img src="/images/hands-on-labs/backup/image3.png" />

Follow the below steps to restore **ProductCatalog** using **Point-in-time-recovery**. 

1.  Sign in to the AWS Management Console and open the DynamoDB console.
    In the navigation pane on the left side of the console, choose
    **Tables**. In the list of tables, choose the ProductCatalog table.
    On the **Backups** tab of the ProductCatalog table, in the
    **Point-in-time recovery** section, choose **Restore to
    point-in-time**.

<img src="/images/hands-on-labs/backup/image4.png" />

2. For the new table name, enter ProductCatalogPITR\_Restore. To confirm
the restorable time, set the **Restore date and time** to the **Latest
restore date**. Choose **Restore** to start the restore process.

  

<img src="/images/hands-on-labs/backup/image5.png" />

The table that is being restored is shown with the status **Restoring**.
After the restore process is finished, the status of the
*ProductCatalogPITR\_Restore* table changes to **Active**.

Note : You can restore the table to the same AWS Region or to a
different Region from where the backup resides. You can also exclude
secondary indexes from being created on the new restored table. In
addition, you can specify a different encryption mode.

<img src="/images/hands-on-labs/backup/image6.png" />

