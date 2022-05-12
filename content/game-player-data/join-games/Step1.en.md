+++
title = "Add users to a game"
menuTitle = "Add users to a game"
date = 2021-04-21T07:33:04-05:00
weight = 51
chapter = false
pre = ""
description = "To get started, you configure your environment and download code that you use during the lab."
+++

The first access pattern you address in this module is adding new users to a game. 

When adding a new user to a game, you need to:
- Confirm that there are not already 50 players in the game (each game can have a maximum of 50 players).
- Confirm that the user is not already in the game.
- Create a new `UserGameMapping` entity to add the user to the game.
- Increment the `people` attribute on the `Game` entity to track how many players are in the game.
 
Note that accomplishing all of these things requires write actions across the existing `Game` entity and the new `UserGameMapping` entity as well as conditional logic for each of the entities. This is the kind of operation that is a perfect fit for DynamoDB transactions because you need to work on multiple entities in the same request, and you want the entire request to succeed or fail together.

In the code you downloaded, a **join_game.py** script is in the **application/** directory. The function in that script uses a DynamoDB transaction to add a user to a game.

```python
import boto3
from entities import Game, UserGameMapping

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
                            "PK": {"S": "GAME#{}".format(game_id) },
                            "SK": {"S": "USER#{}".format(username) },
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
                            "PK": { "S": "GAME#{}".format(game_id) },
                            "SK": { "S": "#METADATA#{}".format(game_id) },
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
        print("Added {} to game {}".format(username, game_id))
    return True

except Exception as e:
    print("Could not add user to game")

join_game_for_user(GAME_ID, USERNAME)
```

In this script’s `join_game_for_user` function, the `transact_write_items()` method performs a write transaction. This transaction has two operations.

In the transaction’s first operation, you use a `Put` operation to insert a new `UserGameMapping` entity. As part of that operation, you specify a condition that the `SK` attribute should not exist for this entity. This ensures that an entity with this `PK` and `SK` doesn’t already exist. If such an entity did already exist, that would mean this user already joined the game.

The second operation is an `Update` operation on the `Game` entity to increment the `people` attribute by one. As part of this operation, you add a conditional check that the current value of `people` is not greater than 50. As soon as 50 people join a game, the game is full and ready to begin.

Run this script with the following command in your terminal:

```sh
python application/join_game.py
```

The output in your terminal should indicate that the user was added to the game.

```text
Added vlopez to game c6f38a6a-d1c5-4bdf-8468-24692ccc4646
```

Note that if you try to run the script again, the function fails. User `vlopez` has been added to the game already, so trying to add the user again does not satisfy the conditions you specified.

The addition of DynamoDB transactions greatly simplifies the workflow around complex operations like these. Without transactions, this would have required multiple API calls with complex conditions and manual rollbacks in the event of conflicts. Now, you can implement such complex operations with fewer than 50 lines of code.
