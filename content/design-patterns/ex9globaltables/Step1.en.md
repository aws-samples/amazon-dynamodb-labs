+++
title = "Step 1 - Create the recommendations table as a global table"
date = 2019-12-02T10:50:03-08:00
weight = 1
+++


Run the following AWS CLI command to create the `recommendations` table in US West (Oregon).
```bash
aws dynamodb create-table --table-name recommendations \
--attribute-definitions AttributeName=customer_id,AttributeType=S AttributeName=category_id,AttributeType=S \
--key-schema AttributeName=customer_id,KeyType=HASH AttributeName=category_id,KeyType=RANGE \
--billing-mode PAY_PER_REQUEST \
--stream-specification StreamEnabled=true,StreamViewType=NEW_AND_OLD_IMAGES \
--region us-west-2 \
--tags Key=workshop-design-patterns,Value=targeted-for-cleanup
```
Create an identical `recommendations` table in US East (N. Virginia).
```bash
aws dynamodb update-table --table-name recommendations --cli-input-json  \
'{
  "ReplicaUpdates":
  [
    {
      "Create": {
        "RegionName": "us-east-1"
      }
    }
  ]
}'
```
Run the following command to wait until the table becomes active.
```bash
aws dynamodb wait table-exists --table-name recommendations
```
You can view the list of replicas created using describe-table.
```bash
aws dynamodb describe-table --table-name recommendations --region us-west-2
```
Let's take a closer look at the `create-table` command. You are creating a table named `recommendations`. The partition key on the table is `customer_id`. The sort key is `category_id`, which contains the movie genre like Drama, Comedy etc.

#### Table: `recommendations`

- Key schema: HASH, RANGE (partition and sort key)
- Table is created in on-demand capacity mode

| Attribute Name (Type)        | Special Attribute?           | Attribute Use Case          | Sample Attribute Value  |
| ------------- |:-------------:|:-------------:| -----:|
| customer_id (STRING)      | Partition Key | Customer ID  | `1`  |
| category_id (STRING)      | Sort key | Category ID   | `Drama`  |

Review the `recommendations` table in the DynamoDB console (as shown in the following screenshot) by choosing the **recommendations** table and then choosing the **Global tables** tab.

![Recommendations table](/images/awsconsole9a.png)

