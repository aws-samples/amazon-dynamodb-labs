+++
title = "Cleaning Up The Resources"
menuTitle = "Cleaning Up The Resources"
date = 2020-04-21T07:38:58-05:00
weight = 66
+++

If you used an account provided by Event Engine, you do not need to do any cleanup. The account terminates when the event is over.

If you used your own account,you might want to clean up what you have created to avoid incurring any unnecessary charges. 


**Step 1: Delete restored AWS resources**

Delete three DynamoDB restored tables using following command.

```bash

aws dynamodb delete-table \
--table-name ProductCatalogODRestore

aws dynamodb delete-table \
--table-name ProductCatalogRestored

aws dynamodb delete-table \
--table-name ProductCatalogPITR


```

**Step 2: Delete the backup plan**

Follow these steps to delete a backup plan:



1. In the AWS Management Console, navigate to **Services -&gt; AWS Backup.** 
In the navigation pane, choose Backup plans.On the Backup plans page, choose *dbBackupPlan*. This takes you to the details page.

![Backup Plan Delete 1](/images/hands-on-labs/backup/backup_plan_delete_1.png)

2. To delete the resource assignments for your plan, choose the radio button next to the dynamodbTable under **Resource assignments**, and then choose **Delete**.

![Backup Plan Delete 2](/images/hands-on-labs/backup/backup_plan_delete_2.png)

3. To delete the backup plan, choose **Delete** in the upper-right corner of the page.

![Backup Plan Delete 3](/images/hands-on-labs/backup/backup_plan_delete_3.png)

4. On the confirmation page, enter *dbBackupPlan*, and choose **Delete plan**.

![Backup Plan Delete 4](/images/hands-on-labs/backup/backup_plan_delete_4.png)
	
**Step 3: Delete the recovery points**



1. On the AWS Backup console, in the navigation pane, choose Backup vaults.

2. On the Backup vaults page, choose the *dynamodb-backup-vault*. Check the recovery point and choose **Delete**.

![Restore Points Delete 1](/images/hands-on-labs/backup/restore_point_delete_1.png)

3. If you are deleting more than one recovery point, follow these steps:

	a. Review the list of recovery points that you are deleting.

    b. If you want to edit the list, choose Modify selection.

    c. If your list contains a continuous backup, choose whether to keep or delete your continuous backup data.

    d. To delete all the recovery points listed, enter delete, and then choose Delete recovery points.

Keep your browser tab open until you see the green success banner at the top of the page.

Prematurely closing this tab will end the deletion process and might leave behind some of the recovery points you wanted to delete.


**Step 4: Delete the backup vault**
1. Select the backup vault *dynamodb-backup-vault* and choose **Delete**. 

![Backup Vault Delete 1](/images/hands-on-labs/backup/backup_vault_delete_1.png)

2. On the confirmation page, enter *dynamodb-backup-vault*, and choose **Delete Backup vault**.

![Backup Vault Delete 2](/images/hands-on-labs/backup/backup_vault_delete_2.png)