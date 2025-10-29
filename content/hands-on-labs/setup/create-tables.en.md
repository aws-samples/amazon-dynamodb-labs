---
title: "Create the DynamoDB Tables"
date: 2021-04-21T07:33:04-05:00
weight: 14
---

We will now create tables (and in a subsequent step load data into them) based on [sample data from the DynamoDB Developer Guide](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/SampleData.html).

Copy the `create-table` commands below and paste them into your AWS Cloud9 command prompt, hitting enter on the last command to execute it. Then use the corresponding `wait` commands by pasting them into the same terminal and running them.

```bash
aws dynamodb create-table \
    --table-name ProductCatalog \
    --attribute-definitions \
        AttributeName=Id,AttributeType=N \
    --key-schema \
        AttributeName=Id,KeyType=HASH \
    --billing-mode PAY_PER_REQUEST \
    --query "TableDescription.TableStatus"
aws dynamodb create-table \
    --table-name Forum \
    --attribute-definitions \
        AttributeName=Name,AttributeType=S \
    --key-schema \
        AttributeName=Name,KeyType=HASH \
    --billing-mode PAY_PER_REQUEST \
    --query "TableDescription.TableStatus"
aws dynamodb create-table \
    --table-name Thread \
    --attribute-definitions \
        AttributeName=ForumName,AttributeType=S \
        AttributeName=Subject,AttributeType=S \
    --key-schema \
        AttributeName=ForumName,KeyType=HASH \
        AttributeName=Subject,KeyType=RANGE \
    --billing-mode PAY_PER_REQUEST \
    --query "TableDescription.TableStatus"
aws dynamodb create-table \
    --table-name Reply \
    --attribute-definitions \
        AttributeName=Id,AttributeType=S \
        AttributeName=ReplyDateTime,AttributeType=S \
    --key-schema \
        AttributeName=Id,KeyType=HASH \
        AttributeName=ReplyDateTime,KeyType=RANGE \
    --billing-mode PAY_PER_REQUEST \
    --query "TableDescription.TableStatus"
```

Run the wait commands. When they all run and end, you can move on:
```bash
aws dynamodb wait table-exists --table-name ProductCatalog
aws dynamodb wait table-exists --table-name Forum
aws dynamodb wait table-exists --table-name Thread
aws dynamodb wait table-exists --table-name Reply
```