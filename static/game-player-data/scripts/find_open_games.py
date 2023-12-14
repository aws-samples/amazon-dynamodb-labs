import boto3
from entities import Game

dynamodb = boto3.client('dynamodb')

def find_open_games():
    resp = dynamodb.scan(
        TableName='battle-royale',
        IndexName="OpenGamesIndex",
    )

    games = [Game(item) for item in resp['Items']]

    return games

games = find_open_games()
print("Open games:")
for game in games:
    print(game)
