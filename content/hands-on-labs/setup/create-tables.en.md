+++
title = "Create the DynamoDB Tables"
date = 2021-04-21T07:33:04-05:00
weight = 14
+++

We will now create tables (and in a subsequent step load data into them) based on [sample data from the DynamoDB Developer Guide](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/SampleData.html).

Copy the `create-table` commands below along with their corresponding `wait` commands and paste them in your AWS Cloud9 command prompt. Each command waits for the table to finish creating. If you get an error from the wait command, you may have submitted it too fast; re-run the wait command in this case.

```bash
aws dynamodb create-table \
    --table-name ProductCatalog \
    --attribute-definitions \
        AttributeName=Id,AttributeType=N \
    --key-schema \
        AttributeName=Id,KeyType=HASH \
    --provisioned-throughput \
        ReadCapacityUnits=10,WriteCapacityUnits=5

aws dynamodb wait table-exists --table-name ProductCatalog

aws dynamodb create-table \
    --table-name Forum \
    --attribute-definitions \
        AttributeName=Name,AttributeType=S \
    --key-schema \
        AttributeName=Name,KeyType=HASH \
    --provisioned-throughput \
        ReadCapacityUnits=10,WriteCapacityUnits=5

aws dynamodb wait table-exists --table-name Forum

aws dynamodb create-table \
    --table-name Thread \
    --attribute-definitions \
        AttributeName=ForumName,AttributeType=S \
        AttributeName=Subject,AttributeType=S \
    --key-schema \
        AttributeName=ForumName,KeyType=HASH \
        AttributeName=Subject,KeyType=RANGE \
    --provisioned-throughput \
        ReadCapacityUnits=10,WriteCapacityUnits=5

aws dynamodb wait table-exists --table-name Thread

aws dynamodb create-table \
    --table-name Reply \
    --attribute-definitions \
        AttributeName=Id,AttributeType=S \
        AttributeName=ReplyDateTime,AttributeType=S \
    --key-schema \
        AttributeName=Id,KeyType=HASH \
        AttributeName=ReplyDateTime,KeyType=RANGE \
    --provisioned-throughput \
        ReadCapacityUnits=10,WriteCapacityUnits=5

aws dynamodb wait table-exists --table-name Reply
```
