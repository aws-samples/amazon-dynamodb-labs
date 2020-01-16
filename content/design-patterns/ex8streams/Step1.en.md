+++
title = "Step 1 - Create the replica table"
date = 2019-12-02T12:34:06-08:00
weight = 1
+++


You can reuse the Python code to create a new table named "logfile_replica" for the replication. Run the following command:
```bash
aws dynamodb create-table --table-name logfile_replica \
--attribute-definitions AttributeName=PK,AttributeType=S AttributeName=GSI_1_PK,AttributeType=S \
--key-schema AttributeName=PK,KeyType=HASH --provisioned-throughput ReadCapacityUnits=10,WriteCapacityUnits=5 \
--tags Key=workshop-design-patterns,Value=targeted-for-cleanup \
--global-secondary-indexes "IndexName=GSI_1,KeySchema=[{AttributeName=GSI_1_PK,KeyType=HASH}],\
Projection={ProjectionType=INCLUDE,NonKeyAttributes=['bytessent', 'requestid', 'host']},\
ProvisionedThroughput={ReadCapacityUnits=10,WriteCapacityUnits=5}"
```
This command will create a new table and an associated GSI with the following definition:

#### Table: logfile_replica

- Key schema: HASH
- Table RCU = 10
- Table WCU = 5
- GSI(s):
  - GSI_1 (10 RCU, 5 WCU) - *Allows for querying by host IP address.*



| Attribute name (Type)        | Special attribute?           | Attribute use case          | Sample attribute value  |
| ------------- |:-------------:|:-------------:| -----:|
| PK (STRING)      | Hash key | Holds the request id  | *request#104009*  |
| GSI_1_PK (STRING)      | GSI 1 hash key | Host  | *host#66.249.67.3*  |


Run the command to wait until the table becomes Active:
```bash
aws dynamodb wait table-exists --table-name logfile_replica
```
