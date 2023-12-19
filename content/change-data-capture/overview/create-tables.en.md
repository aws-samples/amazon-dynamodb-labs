---
title: "Create The DynamoDB Tables"
date: 2023-12-01T00:00:00-00:00
weight: 15
chapter: true
---

Create the DynamoDB tables you will use during the labs for this workshop.

Copy the **create-table** commands below and paste them into your command terminal. Execute the commands to to create two tables named Orders and OrdersHistory.

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
