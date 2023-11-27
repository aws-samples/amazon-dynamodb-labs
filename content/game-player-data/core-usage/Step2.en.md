---
title: "Create the table"
menuTitle: "Create the table"
date: 2021-04-21T07:33:04-05:00
weight: 32
chapter: false
description: "To get started, you configure your environment and download code that you use during the lab."
---

Now that the primary key is designed, let’s create a table.

The code you downloaded in the initial steps include a Python script in the **scripts/** directory named **create_table.py**. The Python script’s contents follow.

```py
import boto3
dynamodb = boto3.client('dynamodb')

try:
    dynamodb.create_table(
        TableName='battle-royale',
        AttributeDefinitions=[
            {
                "AttributeName": "PK",
                "AttributeType": "S"
            },
            {
                "AttributeName": "SK",
                "AttributeType": "S"
            }
        ],
        KeySchema=[
            {
                "AttributeName": "PK",
                "KeyType": "HASH"
            },
            {
                "AttributeName": "SK",
                "KeyType": "RANGE"
            }
        ],
        ProvisionedThroughput={
            "ReadCapacityUnits": 1,
            "WriteCapacityUnits": 1
        }
        )
        print("Table created successfully.")
except Exception as e:
    print("Could not create table. Error:")
    print(e)
```

::alert[Edit **scripts/create_table.py**, set both `ReadCapacityUnits` and `WriteCapacityUnits` to **100** for *battle-royale* table.]

The preceding script uses the [CreateTable](https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_CreateTable.html) operation using [Boto 3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html), the AWS SDK for Python. The operation declares two attribute definitions, which are typed attributes to be used in the primary key. Though DynamoDB is [schemaless](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/SQLtoNoSQL.CreateTable.html), you must declare the names and types of attributes that are used for primary keys. The attributes must be included on every item that is written to the table and thus must be specified as you are creating a table.

Because different entities are stored in a single table, you can’t use primary key attribute names such as `UserId`. The attribute means something different based on the type of entity being stored. For example, the primary key for a user might be its `USERNAME`, and the primary key for a game might be its `GAMEID`. Accordingly, you use generic names for the attributes, such as `PK` (for partition key) and `SK` (for sort key).

After configuring the attributes in the key schema, you specify the [provisioned throughput](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.ReadWriteCapacityMode.html) for the table. DynamoDB has two capacity modes: **provisioned** and **on-demand**. In provisioned capacity mode, you specify exactly the amount of read and write throughput you want. You pay for this capacity whether you use it or not.

In DynamoDB on-demand capacity mode, you pay per request. The cost per request is slightly higher than if you were to use provisioned throughput fully, but you don’t have to spend time doing capacity planning or worrying about getting throttled. On-demand mode works great for spiky or unpredictable workloads. In this lab, provisioned capacity mode is used.

To create the table, run the Python script with the following command in the Cloud9 Terminal.

```sh
python scripts/create_table.py
```

The script should return this message: 
```text
“Table created successfully.”
```