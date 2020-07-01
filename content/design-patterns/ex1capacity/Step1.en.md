+++
title = "Step 1 - Create the DynamoDB table"
date = 2019-12-02T10:26:23-08:00
weight = 2
+++


Run the following AWS CLI command to create the first DynamoDB table called `logfile`:
```bash
aws dynamodb create-table --table-name logfile \
--attribute-definitions AttributeName=PK,AttributeType=S AttributeName=GSI_1_PK,AttributeType=S \
--key-schema AttributeName=PK,KeyType=HASH \
--provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5 \
--tags Key=workshop-design-patterns,Value=targeted-for-cleanup \
--global-secondary-indexes "IndexName=GSI_1,\
KeySchema=[{AttributeName=GSI_1_PK,KeyType=HASH}],\
Projection={ProjectionType=INCLUDE,NonKeyAttributes=['bytessent']},\
ProvisionedThroughput={ReadCapacityUnits=5,WriteCapacityUnits=5}"
````
The table you just created will have the following structure.

#### Table `logfile`:

- Key schema: HASH (partition key)
- Table read capacity units (RCUs) = 5
- Table write capacity units (WCUs) = 5
- Global secondary index (GSI):
  - GSI_1 (5 RCUs, 5 WCUs) - Allows for querying by host IP address.

| Attribute Name (Type)        | Special Attribute?           | Attribute Use Case          | Sample Attribute Value  |
| ------------- |:-------------:|:-------------:| -----:|
| PK (STRING)      | Partition key | Holds the request id for the access log  | *request#104009*  |
| GSI_1_PK (STRING)      | GSI 1 partition key | The host for the request, an IPv4 address  | *host#66.249.67.3*  |

Special attributes include named attributes that define the primary key of a DynamoDB table or a global secondary index (GSI). Global secondary indexes have primary keys just like DynamoDB tables. In DynamoDB, the partition key is the same as the hash key, and the sort key is the same as the range key. The DynamoDB APIs use the terms hash and range, while the AWS documentation uses the terms partition and range. No matter which terms you use, these two keys together form the primary key. To learn more, please review our AWS Developer Guide for Amazon DynamoDB [section on the primary key](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.CoreComponents.html#HowItWorks.CoreComponents.PrimaryKey).

Run the following AWS CLI command to wait until the table becomes `ACTIVE`
```bash
aws dynamodb wait table-exists --table-name logfile
```
You also can run the following AWS CLI command to get only the table status.
```bash
aws dynamodb describe-table --table-name logfile --query "Table.TableStatus"
```
