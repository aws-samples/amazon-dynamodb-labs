---
title: "Create a sparse GSI"
menuTitle: "Create a sparse GSI"
date: 2021-04-21T07:33:04-05:00
weight: 42
chapter: false
description: "To get started, you configure your environment and download code that you use during the lab."
---

In this step, you create the sparse global secondary index (GSI) for open games (games that are not full already).

Creating a GSI is similar to creating a table. In the code you downloaded, you will find a script file in the **scripts/** directory named **add_secondary_index.py**.

```python
import boto3

dynamodb = boto3.client('dynamodb')

try:
    dynamodb.update_table(
        TableName='battle-royale',
        AttributeDefinitions=[
            {
                "AttributeName": "map",
                "AttributeType": "S"
            },
            {
                "AttributeName": "open_timestamp",
                "AttributeType": "S"
            }
        ],
        GlobalSecondaryIndexUpdates=[
            {
                "Create": {
                    "IndexName": "OpenGamesIndex",
                    "KeySchema": [
                        {
                            "AttributeName": "map",
                            "KeyType": "HASH"
                        },
                        {
                            "AttributeName": "open_timestamp",
                            "KeyType": "RANGE"
                        }
                    ],
                    "Projection": {
                        "ProjectionType": "ALL"
                    },
                    "ProvisionedThroughput": {
                        "ReadCapacityUnits": 1,
                        "WriteCapacityUnits": 1
                    }
                }
            }
        ],
    )
    print("Table 'battle-royale' updated successfully.")
except Exception as e:
    print("Could not update table. Error:")
    print(e)
```

::alert[Edit **scripts/add_secondary_index.py**, set both `ReadCapacityUnits` and `WriteCapacityUnits` to **100** for `OpenGamesIndex`.]

Whenever attributes are used in a primary key for a table or secondary index, they must be defined in `AttributeDefinitions`. Then, you `Create` a new GSI in the `GlobalSecondaryIndexUpdates` property. For this GSI, you specify the index name, the schema of the primary key, the provisioned throughput, and the attributes you want to project. 

Note that you do not have to specify that the GSI is intended to be used as a sparse index. That is purely a function of the data you put in. If you write items to your table that do not have the attributes for your secondary indexes, they will not be included in your secondary index.

::alert[You can choose to run either the `add_secondary_index.py` python script or the AWS CLI command below. Both are provided to show different methods of interacting with DynamoDB.]

Create your global secondary index (GSI) by running the following command:

```sh
python scripts/add_secondary_index.py
```

You should see the following message in the console:

```text
Table 'battle-royale' updated successfully.
```

Alternatively, you can create the global secondary index (GSI) by running the AWS CLI command below.

```sh
aws dynamodb update-table \
--table-name battle-royale \
--attribute-definitions AttributeName=map,AttributeType=S AttributeName=open_timestamp,AttributeType=S \
--global-secondary-index-updates \
"[
  {
    \"Create\": {
      \"IndexName\": \"OpenGamesIndex\",
      \"KeySchema\": [
        {
          \"AttributeName\": \"map\",
          \"KeyType\": \"HASH\"
        },
        {
          \"AttributeName\": \"open_timestamp\",
          \"KeyType\": \"RANGE\"
        }
      ],
      \"Projection\": {
        \"ProjectionType\": \"ALL\"
      },
      \"ProvisionedThroughput\": {
        \"ReadCapacityUnits\": 100,
        \"WriteCapacityUnits\": 100
      }
    }
  }
]"
```

If you chose to run the AWS CLI command, you should see output like this:  
Notice that the TableStatus will show as **UPDATING** and the IndexStatus will   show as **CREATING**

```text
{
  "TableDescription": {
    "AttributeDefinitions": [
      {
        "AttributeName": "PK",
        "AttributeType": "S"
      },
      {
        "AttributeName": "SK",
        "AttributeType": "S"
      },
      {
        "AttributeName": "map",
        "AttributeType": "S"
      },
      {
        "AttributeName": "open_timestamp",
        "AttributeType": "S"
      }
    ],
    "TableName": "battle-royale",
    "KeySchema": [
      {
        "AttributeName": "PK",
        "KeyType": "HASH"
      },
      {
        "AttributeName": "SK",
        "KeyType": "RANGE"
      }
    ],
    "TableStatus": "UPDATING",
    "CreationDateTime": "2023-12-06T14:48:31.246000-06:00",
    "ProvisionedThroughput": {
      "NumberOfDecreasesToday": 0,
      "ReadCapacityUnits": 100,
      "WriteCapacityUnits": 100
    },
    "TableSizeBytes": 0,
    "ItemCount": 0,
    "TableArn": "arn:aws:dynamodb:<AWS Region>:<Account ID>:table/battle-royale",
    "TableId": "<Unique ID>",
    "BillingModeSummary": {
      "BillingMode": "PROVISIONED",
      "LastUpdateToPayPerRequestDateTime": "2023-12-07T11:11:34.932000-06:00"
    },
    "GlobalSecondaryIndexes": [
      {
        "IndexName": "OpenGamesIndex",
        "KeySchema": [
          {
            "AttributeName": "map",
            "KeyType": "HASH"
          },
          {
            "AttributeName": "open_timestamp",
            "KeyType": "RANGE"
          }
        ],
        "Projection": {
          "ProjectionType": "ALL"
        },
        "IndexStatus": "CREATING",
        "Backfilling": false,
        "ProvisionedThroughput": {
          "NumberOfDecreasesToday": 0,
          "ReadCapacityUnits": 100,
          "WriteCapacityUnits": 100
        },
        "IndexSizeBytes": 0,
        "ItemCount": 0,
        "IndexArn": "arn:aws:dynamodb:<AWS Region>:<Account ID>:table/battle-royale/index/OpenGamesIndex"
      }
    ],
    "DeletionProtectionEnabled": false
  }
}
```

It will take a few minutes for the new GSI to get populated. You need to wait until the GSI is active. You can find out the current status of the table and its indexes by either way:

- Checking under **Services**, **Database**, **DynamoDB** in the AWS console.

- Running the command below in the Cloud9 Terminal:
    ```sh
    aws dynamodb describe-table --table-name battle-royale --query "Table.GlobalSecondaryIndexes[].IndexStatus"
    ```
    You also can script the command to run every 5 seconds using `watch`.
    ```bash
    # Watch checks every 5 seconds by default
    watch -n 5 "aws dynamodb describe-table --table-name battle-royale --query \"Table.GlobalSecondaryIndexes[].IndexStatus\""
    ```
    Press **Ctrl + C** to end `watch` after the global secondary index has been created.
