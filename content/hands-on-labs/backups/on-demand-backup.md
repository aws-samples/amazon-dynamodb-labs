+++
title = "On-Demand Backup"
menuTitle = "On-Demand Backup"
date = 2021-04-24T07:38:58-05:00
weight = 63
+++


You can use the DynamoDB on-demand backup capability to create full
backups of your tables for long-term retention and archival for
regulatory compliance needs. You can back up and restore your table data
anytime with a single click on the AWS Management Console or with a
single API call. Backup and restore actions run with zero impact on
table performance or availability.

1.  First, go to the [DynamoDB Console](https://console.aws.amazon.com/dynamodbv2/) and click on *Tables* from the side menu.Choose ProductCatalog table.
    On the **Backups** tab of the ProductCatalog table, choose **Create backup**.

<img src="/images/hands-on-labs/backup/image7.png"  />

2.  Make sure that ProductCatalog is the source table name. Enter
    ProductCatalogBackup for the backup name. Choose **Create backup** to
    create the backup.

<img src="/images/hands-on-labs/backup/image8.png"  />

While the backup is being created, the backup status is set to
**Creating**. After the backup is complete, the backup status changes to
**Available**.


**Restore Backup**


1.  go to the [DynamoDB Console](https://console.aws.amazon.com/dynamodbv2/) and click on *Tables* from the side menu.Choose ProductCatalog table.
    Choose **Backups** tab. In the list of backups, choose ProductCatalogBackup.
	Choose **Restore**.

<img src="/images/hands-on-labs/backup/image9.png" />

2.  Enter ProductCatalogODRestore as the new table name. Confirm the
    backup name and other backup details. Choose **Restore**
    to start the restore process. The table that is being restored is
    shown with the status **Creating**. After the restore process is
    finished, the status of the ProductCatalogODRestore table changes to
    **Active**.

<img src="/images/hands-on-labs/backup/image10.png"  />

**To delete a backup**

The following procedure shows how to use the console to delete the
ProductCatalogBackup

1.  go to the [DynamoDB Console](https://console.aws.amazon.com/dynamodbv2/) and click on *Tables* from the side menu.Choose ProductCatalog table.
Choose **Backups** tab. In the list of backups, choose ProductCatalogBackup.
Choose **Delete**:

<img src="/images/hands-on-labs/backup/image11.png"/>

2. Choose **Delete** to delete the backup.

<img src="/images/hands-on-labs/backup/image12.png"  />
