+++
title = "Step 1 - Create a new global secondary index for City-Department"
date = 2019-12-02T12:16:25-08:00
weight = 1
+++


Run the following command to create a new global secondary index called `GSI_3`:
```bash
aws dynamodb update-table --table-name employees \
--attribute-definitions AttributeName=GSI_3_PK,AttributeType=S AttributeName=GSI_3_SK,AttributeType=S \
--global-secondary-index-updates file://gsi_city_dept.json
```
You have to wait until the index has been created before proceeding.

Notice that the following command shows the global secondary index's status as `CREATING`.
```bash
aws dynamodb describe-table --table-name employees --query "Table.GlobalSecondaryIndexes[].IndexStatus"
```
The output looks similar to the following. The order of the table statuses may be different.
```json
[
    "ACTIVE",
    "ACTIVE",
    "CREATING"
]
```
You can script this command to run every two seconds by using ```watch```, 
so that you can more easily see when the table status has changed to `ACTIVE`.
```bash
# Watch checks every two seconds by default
watch -n 2 "aws dynamodb describe-table --table-name employees --query \"Table.GlobalSecondaryIndexes[].IndexStatus\""
```
*Use Ctrl + C to end `watch` after the global secondary index has been created.*

Wait until the new index is ACTIVE before proceeding.
```json
[
    "ACTIVE",
    "ACTIVE",
    "ACTIVE"
]
```
Now you can use the new global secondary index to query the table. You must to use the partition key, and you can use the sort key (but it is optional).

For the sort key, you can use the `begins_with` expression to query 
starting with the left-most attribute of the composite key. 
As a result, you can query all employees in a city or in a specific department in a city.

The ```KeyConditionExpression``` looks like the following.
```py
Key('GSI_3_PK').eq("state#{}".format('TX')) & Key('GSI_3_SK').begins_with('Austin')
```
**Caution**: Wait until the `IndexStatus` is `ACTIVE` on all indexes before continuing. If you try to query a GSI but it is not finished creating, you will receive an error.
