---
title: "Create The DynamoDB Tables"
date: 2023-12-01T00:00:00-00:00
weight: 10
chapter: true
---

In this section you create the DynamoDB tables you will use during the labs for this workshop.

In the commands below, the **create-table** AWS CLI command is used to create two new tables called Orders and OrdersHistory.

It will create the Orders table in provisioned capacity mode to have 5 read capacity units (RCU), 5 write capacity uints (WCU) and a partition key named `id`.

It will also create the OrdersHistory table in provisioned capacity mode to have 5 RCU, 5 WCU, a partition key named `pk` and a sort key named `sk`.

For convenience, the output of the CLI command is stored to a file called `output.log`.

* Copy the **create-table** commands below and paste them into your command terminal. 
* Execute the commands to to create two tables named Orders and OrdersHistory.

```bash
aws dynamodb create-table \
    --table-name Orders \
    --attribute-definitions \
        AttributeName=id,AttributeType=S \
    --key-schema \
        AttributeName=id,KeyType=HASH \
    --provisioned-throughput \
        ReadCapacityUnits=5,WriteCapacityUnits=5 > output.log

aws dynamodb create-table \
    --table-name OrdersHistory \
    --attribute-definitions \
        AttributeName=pk,AttributeType=S \
        AttributeName=sk,AttributeType=S \
    --key-schema \
        AttributeName=pk,KeyType=HASH \
        AttributeName=sk,KeyType=RANGE \
    --provisioned-throughput \
        ReadCapacityUnits=5,WriteCapacityUnits=5 >> output.log
```

Run the command below to confirm that both tables have been created.

```bash        
aws dynamodb wait table-exists --table-name Orders && \
aws dynamodb wait table-exists --table-name OrdersHistory
```
