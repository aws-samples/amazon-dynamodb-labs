import boto3

dynamodb = boto3.client('dynamodb')

GAME_ID = "c6f38a6a-d1c5-4bdf-8468-24692ccc4646"
USERNAME = 'vlopez'


def join_game_for_user(game_id, username):
    try:
        resp = dynamodb.transact_write_items(
            TransactItems=[
                {
                    "Put": {
                        "TableName": "battle-royale",
                        "Item": {
                            "PK": {"S": f"GAME#{game_id}" },
                            "SK": {"S": f"USER#{username}" },
                            "game_id": {"S": game_id },
                            "username": {"S": username }
                        },
                        "ConditionExpression": "attribute_not_exists(SK)",
                        "ReturnValuesOnConditionCheckFailure": "ALL_OLD"
                    },
                },
                {
                    "Update": {
                        "TableName": "battle-royale",
                        "Key": {
                            "PK": { "S": f"GAME#{game_id}" },
                            "SK": { "S": f"#METADATA#{game_id}" },
                        },
                        "UpdateExpression": "SET people = people + :p",
                        "ConditionExpression": "people < :limit",
                        "ExpressionAttributeValues": {
                            ":p": { "N": "1" },
                            ":limit": { "N": "50" }
                        },
                        "ReturnValuesOnConditionCheckFailure": "ALL_OLD"
                    }
                }
            ]
        )
        print(f"Added user: {username} to game: {game_id}")
        return True
    except Exception as e:
        print("Could not add user to game")

join_game_for_user(GAME_ID, USERNAME)
