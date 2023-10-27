---
title: "On-Demand Backup"
menuTitle: "On-Demand Backup"
date: 2021-04-24T07:38:58-05:00
weight: 63
---


You can use the DynamoDB on-demand backup capability to create full
backups of your tables for long-term retention and archival for
regulatory compliance needs. You can back up and restore your table data
anytime with a single click on the AWS Management Console or with a
single API call. Backup and restore actions run with zero impact on
table performance or availability.

1.  First, go to the [DynamoDB Console](https://console.aws.amazon.com/dynamodbv2/) and click on *Tables* from the side menu.Choose ProductCatalog table.
    On the **Backups** tab of the ProductCatalog table, choose **Create backup**.

![OD Backup 1](/images/hands-on-labs/backup/od_backup_1.png)

2.  Make sure that ProductCatalog is the source table name. Choose **Customize settings** and then select **Backup with DynamoDB**. Enter the name `ProductCatalogBackup`. Click **Create backup** to create the backup.

![OD Backup 2](/images/hands-on-labs/backup/od_backup_2.png)

While the backup is being created, the backup status is set to
**Creating**. After the backup is complete, the backup status changes to
**Available**.

### Restore Backup

1.  Go to the [DynamoDB Console](https://console.aws.amazon.com/dynamodbv2/) and click on *Tables* from the side menu.Choose ProductCatalog table.
    Choose **Backups** tab. In the list of backups, choose ProductCatalogBackup.
	Choose **Restore**.

![OD Backup 3](/images/hands-on-labs/backup/od_backup_3.png)

2.  Enter `ProductCatalogODRestore` as the new table name. Confirm the
    backup name and other backup details. Choose **Restore**
    to start the restore process. The table that is being restored is
    shown with the status **Creating**. After the restore process is
    finished, the status of the `ProductCatalogODRestore` table changes to
    **Active**.

![OD Backup 4](/images/hands-on-labs/backup/od_backup_4.png)

### To delete a backup

The following procedure shows how to use the console to delete the
ProductCatalogBackup. You can only delete the backup after the table `ProductCatalogODRestore` is done restoring.

1.  Go to the [DynamoDB Console](https://console.aws.amazon.com/dynamodbv2/) and click on *Tables* from the side menu
1. Choose ProductCatalog table.
1. Choose **Backups** tab.
1. In the list of backups, choose ProductCatalogBackup.
1. Click **Delete**:

![OD Backup 5](/images/hands-on-labs/backup/od_backup_5.png)

Finally, type the world `Delete` and click **Delete** to delete the backup.

![OD Backup 6](/images/hands-on-labs/backup/od_backup_6.png)
