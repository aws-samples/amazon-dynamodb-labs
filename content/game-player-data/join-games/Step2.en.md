---
title: "Start a game"
menuTitle: "Start a game"
date: 2021-04-21T07:33:04-05:00
weight: 52
chapter: false
description: "To get started, you configure your environment and download code that you use during the lab."
---

As soon as a game has 50 users, the creator of the game can start the game to initiate gameplay. In this step, you see how to handle this access pattern.

When the application backend receives a request to start the game, you check three things:
- The game has 50 people signed up.
- The requesting user is the creator of the game.
- The game has not already started.
 
You can handle each of these checks in a [condition expression](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Expressions.ConditionExpressions.html) in a request to update the game. If all of these checks pass, you need to update the entity in the following ways:
- Remove the `open_timestamp` attribute so that it does not appear as an open game in the sparse GSI created earlier.
- Add a `start_time` attribute to indicate when the game started.

In the code you downloaded, a **start_game.py** script is in the **application/** directory.

```python
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
                "PK": { "S": "GAME#{}".format(game_id) },
                "SK": { "S": "#METADATA#{}".format(game_id) }
            },
            UpdateExpression="REMOVE open_timestamp SET start_time = :time",
            ConditionExpression="people = :limit 
                AND creator = :requesting_user 
                AND attribute_not_exists(start_time)",
            ExpressionAttributeValues={
                ":time": { "S": start_time.isoformat() },
                ":limit": { "N": "50" },
                ":requesting_user": { "S": requesting_user }
            },
            ReturnValues="ALL_NEW")
        return Game(resp['Attributes'])
    
    except Exception as e:
        print('Could not start game')
        return False
    
    game = start_game(
        GAME_ID, CREATOR, datetime.datetime(2019, 4, 16, 10, 15, 35)
    )
    
if game:
    print("Started game: {}".format(game))
```

In this script, the `start_game` function is similar to the function you would have in your application. It takes a `game_id`, `requesting_user`, and `start_time`, and it runs a request to update the `Game` entity to start the game.

The `ConditionExpression` parameter in the `update_item()` call specifies each of the three checks that were listed earlier in this step — the game must have 50 people, the user requesting that the game start must be the creator of the game, and the game cannot have a `start_time` attribute, which would indicate it already started.

In the `UpdateExpression` parameter, you can see the changes you want to make to the entity. First you remove the `open_timestamp` attribute from the entity, and then you set the `start_time` attribute to the game’s start time.

::alert[You can choose to run either the `start_game.py` python script or the AWS CLI command below. Both are provided to show different methods of interacting with DynamoDB.]

Run this script in your terminal with the following command:

```shell
python application/start_game.py
```

You should see output in your terminal indicating that the game was started successfully.

```text
Started game: 
Game<c6f38a6a-d1c5-4bdf-8468-24692ccc4646 --Urban Underground>
```

Try to run the script a second time in your terminal. This time, you should see an error message that indicates you could not start the game. This is because you have already started the game, so the `start_time` attribute exists. As a result, the request failed the conditional check on the entity.

Alternatively, you can run this AWS CLI command to start the game:

```sh
aws dynamodb update-item \
--table-name battle-royale \
--key \
"{
  \"PK\": { \"S\": \"GAME#c6f38a6a-d1c5-4bdf-8468-24692ccc4646\" },
  \"SK\": { \"S\": \"#METADATA#c6f38a6a-d1c5-4bdf-8468-24692ccc4646\" }
}" \
--update-expression "REMOVE open_timestamp SET start_time = :time" \
--condition-expression \
"people = :limit 
  AND creator = :requesting_user 
  AND attribute_not_exists(start_time)" \
--expression-attribute-values \
"{
  \":time\": { \"S\": \"2019-04-16T10:15:35\" },
  \":limit\": { \"N\": \"50\" },
  \":requesting_user\": { \"S\": \"gstanley\" }
}" \
--return-values "ALL_NEW"
```

If you run the AWS CLI command, you will see the NEW values of the item you updated and you will notice that there is no longer an attribute named `open_timestamp` but there is an attribute named `start_time`.

```json
{
  "Attributes": {
    "creator": {
      "S": "gstanley"
    },
    "people": {
      "N": "50"
    },
    "SK": {
      "S": "#METADATA#c6f38a6a-d1c5-4bdf-8468-24692ccc4646"
    },
    "create_time": {
      "S": "2019-04-16T10:12:54"
    },
    "map": {
      "S": "Urban Underground"
    },
    "start_time": {
      "S": "2019-04-16T10:15:35"
    },
    "PK": {
      "S": "GAME#c6f38a6a-d1c5-4bdf-8468-24692ccc4646"
    },
    "game_id": {
      "S": "c6f38a6a-d1c5-4bdf-8468-24692ccc4646"
    }
  }
}
```

### Review

In this module, you saw how to satisfy two advanced write operations in the application. First, you used DynamoDB transactions when a user joined a game. With transactions, you handled a complex conditional write across multiple entities in a single request.

Second, you implemented the function for a creator of a game to start a game when it’s ready. In this access pattern, you had an update operation that required checking the value of three attributes and updating two attributes. You can express this complex logic in a single request through the power of condition expressions and update expressions.

In the next module, you will look at the final access pattern, which involves viewing past games in the application.