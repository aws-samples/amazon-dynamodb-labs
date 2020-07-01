+++
title = "Step 1 - Create the replica table"
date = 2019-12-02T12:34:06-08:00
weight = 1
+++

![DynamoDB stream with Lambda](/images/image6.jpg)

Let's create a table named `logfile_replica` to hold the replicated rows. This `create-table` command is based on the command to create the `logfile` table. As a result, it creates a table that can hold the same items as its upstream table.

```bash
aws dynamodb create-table --table-name logfile_replica \
--attribute-definitions AttributeName=PK,AttributeType=S AttributeName=GSI_1_PK,AttributeType=S \
--key-schema AttributeName=PK,KeyType=HASH --provisioned-throughput ReadCapacityUnits=10,WriteCapacityUnits=5 \
--tags Key=workshop-design-patterns,Value=targeted-for-cleanup \
--global-secondary-indexes "IndexName=GSI_1,KeySchema=[{AttributeName=GSI_1_PK,KeyType=HASH}],\
Projection={ProjectionType=INCLUDE,NonKeyAttributes=['bytessent', 'requestid', 'host']},\
ProvisionedThroughput={ReadCapacityUnits=10,WriteCapacityUnits=5}"
```
This command creates a new table and an associated global secondary index with the following definition.

#### Table: `logfile_replica`

- Key schema: HASH (partition key)
- Table read capacity units (RCUs) = 10
- Table write capacity units (WCUs) = 5
- •	Global secondary index:
  - GSI_1 (10 RCUs, 5 WCUs) - Allows for querying by host IP address.



| Attribute Name (Type)        | Special Attribute?           | Attribute Use Case          | Sample Attribute Value  |
| ------------- |:-------------:|:-------------:| -----:|
| PK (STRING)      | Partition key | Holds the request id  | `request#104009`  |
| GSI_1_PK (STRING)      | GSI 1 partition key | Host  | `host#66.249.67.3`  |


Run the following command to wait until the table becomes active.
```bash
aws dynamodb wait table-exists --table-name logfile_replica
```
