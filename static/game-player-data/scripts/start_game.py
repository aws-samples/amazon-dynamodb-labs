import datetime
import boto3
from entities import Game

dynamodb = boto3.client('dynamodb')

GAME_ID = "c6f38a6a-d1c5-4bdf-8468-24692ccc4646"
CREATOR = "gstanley"

def start_game(game_id, requesting_user, start_time):
    try:
        resp = dynamodb.update_item(
            TableName='battle-royale',
            Key={
                "PK": { "S": f"GAME#{game_id}" },
                "SK": { "S": f"#METADATA#{game_id}" }
            },
            UpdateExpression="REMOVE open_timestamp SET start_time = :time",
            ConditionExpression="people = :limit AND creator = :requesting_user AND attribute_not_exists(start_time)",
            ExpressionAttributeValues={
                ":time": { "S": start_time.isoformat() },
                ":limit": { "N": "50" },
                ":requesting_user": { "S": requesting_user }
            },
            ReturnValues="ALL_NEW"
        )
        return Game(resp['Attributes'])
    except Exception as e:
        print('Could not start game')
        return False

game = start_game(GAME_ID, CREATOR, datetime.datetime(2019, 4, 16, 10, 15, 35))

if game:
    print(f"Started game: {game}")
