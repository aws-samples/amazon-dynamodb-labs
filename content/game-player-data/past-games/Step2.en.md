---
title: "Retrieve games for a user"
menuTitle: "Retrieve games for a user"
date: 2021-04-21T07:33:04-05:00
weight: 62
chapter: false
description: "In this step, you add an inverted index to the table. An inverted index is created like any other secondary index."
---

Now that you have created the inverted index, let’s use it to retrieve the `Game` entities played by a `User`. To handle this, you need to query the inverted index with the `User` whose `Game` entities you want to see.

In the code you downloaded, a **find_games_for_user.py** script is in the **scripts/** directory.

```python
import sys
import boto3

from entities import UserGameMapping

dynamodb = boto3.client('dynamodb')

USERNAME = sys.argv[1] if len(sys.argv) == 2 else "carrpatrick"


def find_games_for_user(username):
    try:
        resp = dynamodb.query(
            TableName='battle-royale',
            IndexName='InvertedIndex',
            KeyConditionExpression="SK = :sk",
            ExpressionAttributeValues={
                ":sk": { "S": f"USER#{username}" }
            },
            ScanIndexForward=True
        )
    except Exception as e:
        print('Index is still backfilling. Please try again in a moment.')
        return None

    return [UserGameMapping(item) for item in resp['Items']]

games = find_games_for_user(USERNAME)

if games:
    print(f"Games played by user {USERNAME}:")
    for game in games:
        print(game)
```

In this script, you have a function called `find_games_for_user()` that is similar to a function you would have in your gaming application. This function takes a user name and returns all the games played by the given user.

Run the script in your terminal with the following command:

```sh
python scripts/find_games_for_user.py
```

The script should print all of the games played by the user carrpatrick.

```text
Games played by user carrpatrick:
UserGameMapping: 25cec5bf-e498-483e-9a00-a5f93b9ea7c7   Username: carrpatrick   Place: SILVER
UserGameMapping: c6f38a6a-d1c5-4bdf-8468-24692ccc4646   Username: carrpatrick
UserGameMapping: c9c3917e-30f3-4ba4-82c4-2e9a0e4d1cfd   Username: carrpatrick
```

You can run the script for other users by adding their username as a command line parameter.  
Try running the script again and finding games for user vlopez:

```sh
python scripts/find_games_for_user.py vlopez
```

The output should look like this:

```text
Games played by user vlopez:
UserGameMapping: c6f38a6a-d1c5-4bdf-8468-24692ccc4646   Username: vlopez
```
### Review

In this module, you satisfied the final access pattern by retrieving all `Game` entities played by a `User`. To handle this access pattern, you created a secondary index using the inverted index pattern to allow querying on the other side of the many-to-many relationship between `User` entities and `Game` entities.