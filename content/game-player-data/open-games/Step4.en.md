---
title: "Scan the sparse GSI"
menuTitle: "Scan the sparse GSI"
date: 2021-04-21T07:33:04-05:00
weight: 44
chapter: false
description: "To get started, you configure your environment and download code that you use during the lab."
---

In the previous step, you saw how to find games for a particular map. Some players may prefer to play a specific map, so this is useful. Other players may be willing to play a game at any map. In this section, you learn how to find any open game in the application, regardless of the type of map. To do this, you use the [Scan](https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_Scan.html) API.

In general, you do not want to design your table to use the DynamoDB `Scan` operation because DynamoDB is built for surgical queries that grab the exact entities you need. A `Scan` operation grabs a random collection of entities across your table, so finding the entities you need can require multiple round trips to the database.

However, sometimes `Scan` can be useful. For example, when you have a sparse secondary index, meaning that the index shouldn’t have that many entities in it. In addition, the index includes only those games that are open, and that is exactly what you need.

For this use case, `Scan` works great. Let’s see how it works. In the code you downloaded, a **find_open_games.py** file is in the **application/** directory.

```python
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
```

This code is similar to the code in the previous step. However, rather than using the `query()` method on the DynamoDB client, you use the `scan()` method. Because you are using `scan()`, you don’t need to specify anything about the key conditions like you did with `query()`.DynamoDB returns a bunch of items in no specific order.

Run the script with the following command in your terminal:

```sh
python application/find_open_games.py
```

Your terminal should print a list of nine games that are open across a variety of maps.

```text
Open games:
Game<c6f38a6a-d1c5-4bdf-8468-24692ccc4646 --Urban Underground>
Game<d06af94a-2363-441d-a69b-49e3f85e748a --Dirty Desert>
Game<873aaf13-0847-4661-ba26-21e0c66ebe64 --Dirty Desert>
Game<fe89e561-8a93-4e08-84d8-efa88bef383d --Dirty Desert>
Game<248dd9ef-6b17-42f0-9567-2cbd3dd63174 --Juicy Jungle>
Game<14c7f97e-8354-4ddf-985f-074970818215 --Green Grasslands>
Game<3d4285f0-e52b-401a-a59b-112b38c4a26b --Green Grasslands>
Game<683680f0-02b0-4e5e-a36a-be4e00fc93f3 --Green Grasslands>
Game<0ab37cf1-fc60-4d93-b72b-89335f759581 --Green Grasslands>
```

Again, using [PartiQL](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/ql-reference.html), you can run a `Scan index` query to receive a similar result.  
Click on the 3 dots (...) next to the OpenGamesIndex and choose **Scan index**.

![PartiQL editor in the AWS console](/static/images/game-player-data/open-games/aws-console-dynamodb-battle-royale-partiql-editor.png)

In this step, you saw how using the `Scan` operation can be the right choice in specific circumstances. You used `Scan` to grab an assortment of entities from the sparse global secondary index (GSI) to show open games to players.

### Review

In this module, you added a global secondary index (GSI) to the table. This satisfied two additional access patterns:

- Find open games by map (Read)
- Find open games (Read)


To accomplish this, you used a sparse index that included only the games that were still open for additional players. You then used both the `Query` and `Scan` APIs against the index to find open games. 

In the next module, you will use DynamoDB transactions as you add new players to a game and close games when they are full.