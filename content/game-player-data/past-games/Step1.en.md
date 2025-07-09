---
title: "Add an inverted index"
menuTitle: "Add an inverted index"
date: 2021-04-21T07:33:04-05:00
weight: 61
chapter: false
description: "In this step, you add an inverted index to the table. An inverted index is created like any other secondary index."
---

In this step, you add an inverted index to the table. An inverted index is created like any other global secondary index (GSI).

In the code you downloaded, a **add_inverted_index.py** script is in the **scripts/** directory. This Python script adds an inverted index to your table.

```python
import boto3

dynamodb = boto3.client('dynamodb')

try:
    dynamodb.update_table(
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
        GlobalSecondaryIndexUpdates=[
            {
                "Create": {
                    "IndexName": "InvertedIndex",
                    "KeySchema": [
                        {
                            "AttributeName": "SK",
                            "KeyType": "HASH"
                        },
                        {
                            "AttributeName": "PK",
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

::alert[Edit **scripts/add_inverted_index.py**, set both `ReadCapacityUnits` and `WriteCapacityUnits` to **100** for `InvertedIndex`.]

In this script, you call an `update_table()` method on the DynamoDB client. In the method, you pass details about the secondary index you want to create, including the key schema for the index, the provisioned throughput, and the attributes to project into the index. 

::alert[You can choose to run either the `add_inverted_index.py` python script or the AWS CLI command below. Both are provided to show different methods of interacting with DynamoDB.]

Run the script by typing the following command in your terminal:

```sh
python scripts/add_inverted_index.py
```

Your terminal will display output that your index was created successfully.

```text
Table 'battle-royale' updated successfully.
```

Alternatively, you can create the `InvertedIndex` GSI by running the AWS CLI command below:

```sh
aws dynamodb update-table \
--table-name battle-royale \
--attribute-definitions AttributeName=PK,AttributeType=S AttributeName=SK,AttributeType=S \
--global-secondary-index-updates \
"[
  {
    \"Create\": {
      \"IndexName\": \"InvertedIndex\",
      \"KeySchema\": [
        {
          \"AttributeName\": \"SK\",
          \"KeyType\": \"HASH\"
        },
        {
          \"AttributeName\": \"PK\",
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

If you chose to run the AWS CLI command, the output will contain a full description of the `battle-royale` table including existing and newly creating indexes. You will notice the IndexStatus for the index `InvertedIndex` will show as **CREATING**.

It will take a few minutes for the new secondary index to get populated. You need to wait until the secondary index is active. 

You can find out the current status of the table and its indexes by either way:
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