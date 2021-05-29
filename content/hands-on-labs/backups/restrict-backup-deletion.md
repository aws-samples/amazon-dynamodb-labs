+++
title = "Restrict backup deletion"
menuTitle = "Restrict Backup Deletion"
date = 2020-04-21T07:38:58-05:00
weight = 65
+++

Customer has a common ask when they want their developer/admin should be
allowed to create and delete DynamoDB tables but they shouldn’t be
allowed to delete the backups.

You can achieve this by creating IAM policy. Following is an example of
the AWS IAM policy which allow “Create Table”, “List Table”, “Create
Backup” and “Delete Table” and denies “Delete Backup” of DynamoDB table.

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
Refer the below documentation for more details:-

<https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/backuprestore_IAM.html>

You can restrict in AWS backup by denying as well by denying
“DeleteBackupSelection” in IAM policy.

```json

{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "backup:DeleteBackupSelection",
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
You can apply the policy to role and assign the role to IAM group. Now
user belong to this IAM group will inherit the permission.

Let’s say now user tries to delete the backup in AWS backup.

<img src="/images/hands-on-labs/backup/image29.png" />

User gets the access denied error due to insufficient permission to
delete the backup.

<img src="/images/hands-on-labs/backup/image30.png"/>

