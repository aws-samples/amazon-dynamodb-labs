import sys
import boto3
from entities import Game

dynamodb = boto3.client('dynamodb')

MAP_NAME = sys.argv[1] if len(sys.argv) == 2 else "Green Grasslands"

def find_open_games_by_map(map_name):
    resp = dynamodb.query(
        TableName='battle-royale',
        IndexName="OpenGamesIndex",
        KeyConditionExpression="#map = :map",
        ExpressionAttributeNames={
            "#map": "map"
        },
        ExpressionAttributeValues={
            ":map": { "S": map_name },
        },
        ScanIndexForward=True
    )

    games = [Game(item) for item in resp['Items']]

    return games

games = find_open_games_by_map(MAP_NAME)
print(f"Open games for map: {MAP_NAME}:")
for game in games:
    print(game)
