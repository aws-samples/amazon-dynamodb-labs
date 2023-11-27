---
title: "Bulk-load data"
menuTitle: "Bulk-load data"
date: 2021-04-21T07:33:04-05:00
weight: 33
chapter: false
description: "To get started, you configure your environment and download code that you use during the lab."
---


In this step, you bulk-load some data into the DynamoDB you created in the preceding step. This means that in succeeding steps, you will have sample data to use.

In the **scripts/directory**, you will find a file called **items.json**. This file contains 835 example items that were randomly generated for this lab. These items include `User`, `Game`, and `UserGameMapping` entities. Open the file if you want to see some of the example items.

The **scripts/** directory also has a file called **bulk_load_table.py** that reads the items in the **items.json** file and bulk-writes them to the DynamoDB table. Below is the content of the file:

```python
import json
import boto3
dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table('battle-royale')
items = []

with open('scripts/items.json', 'r') as f:
    for row in f:
        items.append(json.loads(row))
        
with table.batch_writer() as batch:
    for item in items:
        batch.put_item(Item=item)
```

In this script, rather than using the low-level client in Boto 3, you use a higher-level [Resource object](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/migration.html#resource-objects). Resource objects provide an easier interface for using the AWS APIs. The Resource object is useful in this situation because it batches the requests. The [BatchWriteItem](https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_BatchWriteItem.html) operation accepts as many as 25 items in a single request. The Resource object handles that batching for you rather than making you divide the data into requests of 25 or fewer items.

Run the **bulk_load_table.py** script and load your table with data by running the following command in the terminal:

```sh
python scripts/bulk_load_table.py
```

You can ensure that all your data was loaded into the table by running a `Scan` operation and getting the count.

```sh
aws dynamodb scan --table-name battle-royale --select COUNT --return-consumed-capacity TOTAL
```

This should display the following results:

```json
{
    "Count": 835, 
    "ScannedCount": 835, 
    "ConsumedCapacity": {
        "CapacityUnits": 14.5, 
        "TableName": "battle-royale", 
        "Table": {
            "CapacityUnits": 14.5
        }
    }
}
```

You should see a `Count` of 835, indicating that all of your items were loaded successfully.

You can also browse the table by navigating to **Services** -> **Database** -> **DynamoDB** in the AWS console.

![BaseTableConsole](/static/images/game-player-data/core-usage/basetable-consolev2.png)

In the next step, you see how to retrieve multiple entity types in a single request, which can reduce the total network requests you make in your application and enhance application performance.