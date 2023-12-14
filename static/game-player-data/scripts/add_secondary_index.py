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
