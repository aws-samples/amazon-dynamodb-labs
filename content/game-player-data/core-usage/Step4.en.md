+++
title = "Retrive Item collections"
menuTitle = "Retrive Item collections"
date = 2021-04-21T07:33:04-05:00
weight = 34
chapter = false
pre = ""
description = "To get started, you configure your environment and download code that you use during the lab."
+++

An **Item collection** is a set of items with the same partition key value but different sort key values where the items of different entity types have relationships with the partition key.

As you read in the previous module, you should optimize DynamoDB tables for the number of requests it receives. It was also mentioned that DynamoDB does not have joins that a relational database has. Instead, you design your table to allow for join-like behavior in your requests.

In this step, you retrieve multiple entity types in a single request. In the gaming application, you may want to fetch details about a game. These details include information about the game itself such as the time it started, time it ended, and details about the users that played in the game.

This request spans two entity types: the `Game` entity and the `UserGameMapping` entity. However, this doesn’t mean you need to make multiple requests.

In the code you downloaded, a **fetch_game_and_players.py** script is in the **application/** directory. This script shows how you can structure your code to retrieve both the `Game` entity and the `UserGameMapping` entity for the game in a single request.

The following code composes the **fetch_game_and_players.py** script:

```python
import boto3
from entities import Game, UserGameMapping

dynamodb = boto3.client('dynamodb')

GAME_ID = "3d4285f0-e52b-401a-a59b-112b38c4a26b"

def fetch_game_and_users(game_id):
    resp = dynamodb.query(
        TableName='battle-royale',
        KeyConditionExpression="PK = :pk AND SK BETWEEN :metadata 
            AND :users",
        ExpressionAttributeValues={
            ":pk": { "S": "GAME#{}".format(game_id) },
            ":metadata": { "S": "#METADATA#{}".format(game_id) },
            ":users": { "S": "USER$" },
        },
        ScanIndexForward=True
    )
    game = Game(resp['Items'][0])
    game.users = [UserGameMapping(item) for item in resp['Items'][1:]]
    
    return game
    
game = fetch_game_and_users(GAME_ID)

print(game)
for user in game.users:
    print(user)
```

At the beginning of this script, you import the Boto 3 library and some simple classes to represent the objects inthe application code. You can see the definitions for those entities in the **application/entities.py** file.

The real work of the script happens in the `fetch_game_and_users` function that’s defined in the module. This is similar to a function you would define in your application to be used by any endpoints that need this data.

The `fetch_game_and_users` function does a few things. First, it makes a `Query` request to DynamoDB. This `Query` uses a `PK` of `GAME#<GameId>`. Then, it requests any entities where the sort key is between `#METADATA#<GameId>` and `USER$`. This grabs the `Game` entity, whose sort key is `#METADATA#<GameId>`, and all `UserGameMapping` entities, whose keys start with `USER#`. Sort keys of the string type are sorted by ASCII character codes. The dollar sign ($) comes directly after the pound sign (#) in [ASCII](http://support.ecisolutions.com/doc-ddms/help/reportsmenu/ascii_sort_order_chart.htm), so this ensures that you will get all mappings in the `UserGameMapping` entity.

When you receive a response, you assemble the data entities into objects known by the application. You know that the first entity returned is the `Game` entity, so you create a `Game` object from the entity. For the remaining entities, you create a `UserGameMapping` object for each entity and then attach the array of users to the `Game` object.

The end of the script shows the usage of the function and prints out the resulting objects.

You can run the script in the Cloud9 Terminal with the following command:

```sh
python application/fetch_game_and_players.py
```

The script should print the `Game` object and all `UserGameMapping` objects to the console.

```text
Game<3d4285f0-e52b-401a-a59b-112b38c4a26b --Green Grasslands>
UserGameMapping<3d4285f0-e52b-401a-a59b-112b38c4a26b --branchmichael>
UserGameMapping<3d4285f0-e52b-401a-a59b-112b38c4a26b --deanmcclure>
UserGameMapping<3d4285f0-e52b-401a-a59b-112b38c4a26b --emccoy>
UserGameMapping<3d4285f0-e52b-401a-a59b-112b38c4a26b --emma83>
UserGameMapping<3d4285f0-e52b-401a-a59b-112b38c4a26b --iherrera>
UserGameMapping<3d4285f0-e52b-401a-a59b-112b38c4a26b --jeremyjohnson>
UserGameMapping<3d4285f0-e52b-401a-a59b-112b38c4a26b --lisabaker>
UserGameMapping<3d4285f0-e52b-401a-a59b-112b38c4a26b --maryharris>
UserGameMapping<3d4285f0-e52b-401a-a59b-112b38c4a26b --mayrebecca>
UserGameMapping<3d4285f0-e52b-401a-a59b-112b38c4a26b --meghanhernandez>
UserGameMapping<3d4285f0-e52b-401a-a59b-112b38c4a26b --nruiz>
UserGameMapping<3d4285f0-e52b-401a-a59b-112b38c4a26b --pboyd>
UserGameMapping<3d4285f0-e52b-401a-a59b-112b38c4a26b --richardbowman>
UserGameMapping<3d4285f0-e52b-401a-a59b-112b38c4a26b --roberthill>
UserGameMapping<3d4285f0-e52b-401a-a59b-112b38c4a26b --robertwood>
UserGameMapping<3d4285f0-e52b-401a-a59b-112b38c4a26b --victoriapatrick>
UserGameMapping<3d4285f0-e52b-401a-a59b-112b38c4a26b --waltervargas>
```

This script shows how you can model your table and write your queries to retrieve multiple entity types in a single DynamoDB request. In a relational database, you use joins to retrieve multiple entity types from different tables in a single request. With DynamoDB, you specifically model your data, so that entities you should access together are located next to each other in a single table. This approach replaces the need for joins in a typical relational database and keeps your application high-performing as you scale up.


### Review

In this module, you designed a primary key and created a table. Then, you bulk-loaded data into the table and saw how to query for multiple entity types in a single request.

With the current primary key design, you can satisfy the following access patterns:

- Create user profile (Write)

- Update user profile (Write)

- Get user profile (Read)

- Create game (Write)

- View game (Read)

- Join game for a user (Write)

- Start game (Write)

- Update game for a user (Write)

- Update game (Write)