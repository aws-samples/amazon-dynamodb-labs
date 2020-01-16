+++
title = "Step 1 - Add a new GSI to the table employees"
date = 2019-12-02T10:57:23-08:00
weight = 1
+++


Execute the code to add a new GSI using the attribute is_manager as the GSI Partition Key, stored under the attribute named "GSI_2_PK". The employee job title is stored under "GSI_2_SK".

```bash
aws dynamodb update-table --table-name employees \
--attribute-definitions AttributeName=GSI_2_PK,AttributeType=S AttributeName=GSI_2_SK,AttributeType=S \
--global-secondary-index-updates file://gsi_manager.json
```
You need to wait until the index has been created. This step will take roughly 5 minutes.

If you run the following command and "IndexStatus": "CREATING" you will need to wait more time until the all the "IndexStatus": "ACTIVE"
```code
aws dynamodb describe-table --table-name employees --query "Table.GlobalSecondaryIndexes[].IndexStatus"
```
Output:
```json
[
    "CREATING",
    "ACTIVE"
]
```
You can script the command to run every 2 seconds using watch. Let's do that:
```bash
# Watch checks every 2 seconds by default
watch -n 2 "aws dynamodb describe-table --table-name employees --query \"Table.GlobalSecondaryIndexes[].IndexStatus\""
```
*Use Ctrl + C to end ```watch``` when the GSI is done creating.*

Wait until the new index is ```ACTIVE``` before proceeding:
```json
[
    "ACTIVE",
    "ACTIVE"
]
```
**Warning**: *Do not continue until the IndexStatus is ACTIVE on both indexes*
