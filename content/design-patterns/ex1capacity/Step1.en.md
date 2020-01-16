+++
title = "Step 1 - Create the DynamoDB table"
date = 2019-12-02T10:26:23-08:00
weight = 2
+++


Run the following AWS CLI command to create the first DynamoDB table called 'logfile':
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

#### Table logfile:

- Key schema: HASH
- Table RCU = 5
- Table WCU = 5
- GSI(s):
  - GSI_1 (5 RCU, 5 WCU) - *Allows for querying by host IP address.*

| Attribute name (Type)        | Special attribute?           | Attribute use case          | Sample attribute value  |
| ------------- |:-------------:|:-------------:| -----:|
| PK (STRING)      | Hash key | Holds the request id for the access log  | *request#104009*  |
| GSI_1_PK (STRING)      | GSI 1 hash key | The host for the request, an IPv4 address  | *host#66.249.67.3*  |


Run the command to wait until the table becomes Active:
```bash
aws dynamodb wait table-exists --table-name logfile
```
You can also run the following command to get only the table status:
```bash
aws dynamodb describe-table --table-name logfile --query "Table.TableStatus"
```
