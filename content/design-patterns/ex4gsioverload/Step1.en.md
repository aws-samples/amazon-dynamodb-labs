+++
title = "Step 1 - Create the Employees table for GSI overloading"
date = 2019-12-02T10:50:03-08:00
weight = 1
+++


Run the AWS CLI command to create the table:
```bash
aws dynamodb create-table --table-name employees \
--attribute-definitions AttributeName=PK,AttributeType=S AttributeName=SK,AttributeType=S \
AttributeName=GSI_1_PK,AttributeType=S AttributeName=GSI_1_SK,AttributeType=S \
--key-schema AttributeName=PK,KeyType=HASH AttributeName=SK,KeyType=RANGE \
--provisioned-throughput ReadCapacityUnits=100,WriteCapacityUnits=100 \
--tags Key=workshop-design-patterns,Value=targeted-for-cleanup \
--global-secondary-indexes "IndexName=GSI_1,\
KeySchema=[{AttributeName=GSI_1_PK,KeyType=HASH},{AttributeName=GSI_1_SK,KeyType=RANGE}],\
Projection={ProjectionType=ALL},\
ProvisionedThroughput={ReadCapacityUnits=100,WriteCapacityUnits=100}"
```
Run the command to wait until the table becomes Active:
```bash
aws dynamodb wait table-exists --table-name employees
```
Lets take a closer look at this create-table command. You are creating a table named "employees". The Partition key on the table is "PK" and it will hold the **employee ID**. The Sort key is "SK" which will contain a derived value we will choose in the python script. We will revisit this shortly. We will also create a GSI on this table and we will name this index as "GSI_1" and it will be an overloaded GSI. The partition key on the GSI is "GSI_1_PK", and will hold the same value as the sort key "SK" on the base table. The GSI_1 sort key value is **name**, and its attribute name will be "GSI_1_SK".

#### Table: employees

- Key schema: HASH, RANGE
- Table RCU = 100
- Table WCU = 100
- GSI(s):
  - GSI_1 (100 RCU, 100 WCU) - *Allows for querying by host IP address.*



| Attribute name (Type)        | Special attribute?           | Attribute use case          | Sample attribute value  |
| ------------- |:-------------:|:-------------:| -----:|
| PK (STRING)      | Hash key | Holds the employee id  | *e#129*  |
| SK (STRING)      | Sort key | Derived value  | *master*, *state#MI*  |
| GSI_1_PK (STRING)      | GSI 1 hash key | Derived value  | *master*, *state#MI* |
| GSI_1_SK (STRING)      | GSI 1 sort key | Employee name  | *Christine Milsted*  |
