---
title: "Restrict backup deletion"
menuTitle: "Restrict Backup Deletion"
date: 2020-04-21T07:38:58-05:00
weight: 65
---

Customers often request that their developers or administrators be allowed to create and delete DynamoDB tables, but not be permitted to delete the backups.

This can be achieved by creating an IAM policy. The following is an example of an AWS IAM policy that allows “Create Table,” “List Tables,” “Create Backup,” and “Delete Table”, while denying the “Delete Backup” action on DynamoDB tables.

```json

{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "dynamodb:CreateTable",
                "dynamodb:CreateBackup",
                "dynamodb:DeleteTable"
            ],
            "Resource": "arn:aws:dynamodb:us-east-1:123456789:table/*"
        },
        {
            "Sid": "VisualEditor1",
            "Effect": "Allow",
            "Action": "dynamodb:ListTables",
            "Resource": "*"
        },
        {
            "Sid": "VisualEditor2",
            "Effect": "Deny",
            "Action": "dynamodb:DeleteBackup",
            "Resource": "arn:aws:dynamodb:us-east-1:123456789:table/*/backup/*"
        }
    ]
}


```
[At this documentation page you will find out more about using IAM with DynamoDB backups](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/backuprestore_IAM.html)



You can also restrict backup deletion in AWS Backup by adding an explicit Deny statement for the “DeleteBackupSelection” Action in an IAM policy.

```json

{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "backup:CreateBackupSelection",
                "backup:StartBackupJob",
                "backup:CreateBackupPlan",
                "backup:ListBackupSelections",
                "backup:ListRecoveryPointsByBackupVault",
                "backup:GetBackupVaultAccessPolicy",
                "backup:GetBackupSelection"
            ],
            "Resource": [
                "arn:aws:backup:us-east-1:123456789:backup-plan:*",
                "arn:aws:backup:us-east-1:123456789:backup-vault:*"
            ]
        },
        {
            "Sid": "VisualEditor1",
            "Effect": "Deny",
            "Action": "backup:DeleteBackupSelection",
            "Resource": "arn:aws:backup:us-east-1:123456789:backup-plan:*"
        }
    ]
}


```
You can apply the policy to a role and assign the role to an IAM group, so users belonging to the IAM group inherit the permission.

If a user now tries to delete the backup in AWS backup, they will received an access denied error due to insufficient permissions to
delete the backup.

:image[Restrict Backup Deletion 1]{src="/static/images/hands-on-labs/backup/restrict_delete_1.png" disableZoom=true width=1150}

:image[Restrict Backup Deletion 2]{src="/static/images/hands-on-labs/backup/restrict_delete_2.png" disableZoom=true width=1050}
