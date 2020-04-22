+++
title = "Step 1 - Add a new global secondary index to the employees table"
date = 2019-12-02T10:57:23-08:00
weight = 1
+++


Add a new global secondary index that uses the `is_manager` attribute as the global secondary index partition key, which is stored under the attribute named `GSI_2_PK`. Employee job titles are stored under `GSI_2_SK`.

Run the following AWS CLI command.

```bash
aws dynamodb update-table --table-name employees \
--attribute-definitions AttributeName=GSI_2_PK,AttributeType=S AttributeName=GSI_2_SK,AttributeType=S \
--global-secondary-index-updates file://gsi_manager.json
```
Wait until the global secondary index has been created. This takes approximately 5 minutes.

Check output of the following command. If "`IndexStatus`": is "`CREATING`" you will have to wait until "`IndexStatus`" is "`ACTIVE`" before continuing to the next step.

```bash
aws dynamodb describe-table --table-name employees --query "Table.GlobalSecondaryIndexes[].IndexStatus"
```
The output will initially look like the following.
```json
[
    "CREATING",
    "ACTIVE"
]
```
You also can script the command to run every 2 seconds using `watch`.
```bash
# Watch checks every 2 seconds by default
watch -n 2 "aws dynamodb describe-table --table-name employees --query \"Table.GlobalSecondaryIndexes[].IndexStatus\""
```
Press **Ctrl + C** to end `watch` after the global secondary index has been created.

Wait until the new index is `ACTIVE` before proceeding.
```json
[
    "ACTIVE",
    "ACTIVE"
]
```
**Caution:** Do not continue until the `IndexStatus` is `ACTIVE` on both indexes. Querying the index before it is `ACTIVE` will result in a failed query.
