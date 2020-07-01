+++
title = "Step 1 - Create the employees table for global secondary index key overloading"
date = 2019-12-02T10:50:03-08:00
weight = 1
+++


Run the following AWS CLI command to create the `employees` table.
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
Run the following command to wait until the table becomes active.
```bash
aws dynamodb wait table-exists --table-name employees
```
Let's take a closer look at the `create-table` command. You are creating a table named `employees`. The partition key on the table is `PK` and it holds the employee ID. The sort key is `SK`, which contains a derived value that you choose in the Python script. (We'll revisit this shortly.) You will create a global secondary index on this table and name it `GSI_1`; This will be an overloaded global secondary index. The partition key on the global secondary index is `GSI_1_PK`, and holds the same value as the sort key `SK` on the base table. The `GSI_1` sort key value is `name`, and its attribute name is `GSI_1_SK`.

#### Table: `employees`

- Key schema: HASH, RANGE (partition and sort key)
- Table read capacity units (RCUs) = 100
- Table write capacity units (WCUs)  = 100
- Global secondary index:
  - GSI_1 (100 RCUs, 100 WCUs) - Allows for querying by host IP address.



| Attribute Name (Type)        | Special Attribute?           | Attribute Use Case          | Sample Attribute Value  |
| ------------- |:-------------:|:-------------:| -----:|
| PK (STRING)      | Partition Key | Employee ID  | `e#129`  |
| SK (STRING)      | Sort key | Derived value  | `root`, `state#MI`  |
| GSI_1_PK (STRING)      | GSI_1 partition key | Derived value  | `root`, `state#MI` |
| GSI_1_SK (STRING)      | GSI_1 sort key | Employee name  | `Christine Milsted`  |
