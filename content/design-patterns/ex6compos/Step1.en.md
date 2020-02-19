+++
title = "Step 1 - Creating a new GSI for City-Department"
date = 2019-12-02T12:16:25-08:00
weight = 1
+++


You can run the following command to create the new GSI gsicitydept:
```bash
aws dynamodb update-table --table-name employees \
--attribute-definitions AttributeName=GSI_3_PK,AttributeType=S AttributeName=GSI_3_SK,AttributeType=S \
--global-secondary-index-updates file://gsi_city_dept.json
```
You need to wait until the index has been created.

Notice that the GSI is currently in ```CREATING```:
```bash
aws dynamodb describe-table --table-name employees --query "Table.GlobalSecondaryIndexes[].IndexStatus"
```
Output:
```json
[
    "ACTIVE",
    "ACTIVE",
    "CREATING"
]
```
You can script the command to run every 2 seconds using watch. Let's do that:
```bash
# Watch checks every 2 seconds by default
watch -n 2 "aws dynamodb describe-table --table-name employees --query \"Table.GlobalSecondaryIndexes[].IndexStatus\""
```
*Use Ctrl + C to end ```watch``` when the GSI is done creating.*

Wait until the new index is ACTIVE before proceeding:
```json
[
    "ACTIVE",
    "ACTIVE",
    "ACTIVE"
]
```
Now you can use the new GSI to query the table. You must use the Partition-Key and you can optionally use the Sort-Key.

For the Sort-Key you can use the **begins_with** expression to query starting with the left-most attribute of the composite key. Thus, you can query all employees within a city or within a specific department in the city.

The KeyConditionExpression will look like this:
```py
Key('GSI_3_PK').eq("state#{}".format('TX')) & Key('GSI_3_SK').begins_with('Indianapolis')
```
**Warning**: *Wait until the IndexStatus is ```ACTIVE``` on all indexes before continuing*
