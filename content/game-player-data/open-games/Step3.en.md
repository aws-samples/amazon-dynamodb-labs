---
title: "Query the sparse GSI"
menuTitle: "Query the sparse GSI"
date: 2021-04-21T07:33:04-05:00
weight: 43
chapter: false
pre: ""
description: "To get started, you configure your environment and download code that you use during the lab."
---

Now that you have configured the GSI, let’s use it to satisfy some of the access patterns.

To use a secondary index, there are two API calls available: `Query` and `Scan`. With `Query`, you must specify the partition key, and it returns a targeted result. With Scan, you don’t specify a partition key, and the operation runs across your entire table. Scans are discouraged in DynamoDB except in specific circumstances because they access *every* item in your database. If you have a significant amount of data in your table, scanning can take a very long time. In the next step, you see why Scans can be a powerful tool when used with sparse indexes.

You can use the `Query` API against the global secondary index (GSI) you created in the previous step to find all open games by map name. The GSI is partitioned by `map` name, allowing you to make targeted queries to find open games.

In the code you downloaded, a **find_open_games_by_map.py** file is in the **application/** directory.

```python
import boto3
from entities import Game

dynamodb = boto3.client('dynamodb')

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
    
games = find_open_games_by_map("Green Grasslands")
for game in games:
    print(game)
```

In the preceding script, the `find_open_games_by_map` function is similar to a function you would have in your application. The function accepts a map name and makes a query against the `OpenGamesIndex` to find all open games for the map. It then assembles the returned entities into `Game` objects that can be used in your application.

Execute this script by running the following command in your terminal:

```sh
python application/find_open_games_by_map.py
```

The terminal will show the following output with four open games for the Green Grasslands map.

```text
Open games for Green Grasslands:
Game<14c7f97e-8354-4ddf-985f-074970818215 --Green Grasslands>
Game<3d4285f0-e52b-401a-a59b-112b38c4a26b --Green Grasslands>
Game<683680f0-02b0-4e5e-a36a-be4e00fc93f3 --Green Grasslands>
Game<0ab37cf1-fc60-4d93-b72b-89335f759581 --Green Grasslands>
```