---
title: "Inserting/Updating Data"
date: 2020-04-21T07:38:58-05:00
weight: 24
---

## Inserting Data

The DynamoDB [PutItem API](https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_PutItem.html) is used to create a new item or to replace existing items completely with a new item.  It is invoked using the [put-item CLI command](https://docs.aws.amazon.com/cli/latest/reference/dynamodb/put-item.html).

Let's say we wanted to insert a new item into the *Reply* table:

```bash
aws dynamodb put-item \
    --table-name Reply \
    --item '{
        "Id" : {"S": "Amazon DynamoDB#DynamoDB Thread 2"},
        "ReplyDateTime" : {"S": "2021-04-27T17:47:30Z"},
        "Message" : {"S": "DynamoDB Thread 2 Reply 3 text"},
        "PostedBy" : {"S": "User C"}
    }' \
    --return-consumed-capacity TOTAL
```

We can see in the response that this request consume 1 WCU:

```json
{
    "ConsumedCapacity": {
        "TableName": "Reply",
        "CapacityUnits": 1.0
    }
}
```

## Updating Data

The DynamoDB [UpdateItem API](https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_UpdateItem.html) is used to create a new item or to replace existing items completely with a new item.  It is invoked using the [update-item CLI command](https://docs.aws.amazon.com/cli/latest/reference/dynamodb/update-item.html).  This API requires you to specify the full Primary Key and can selectively modify specific attributes without changing others(you don't need to pass in the full item).

The `update-item` API call also allows you to specify a ConditionExpression, meaning the Update request will only execute if the ConditionExpression is satisfied.  For more information please see [Condition Expressions](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Expressions.ConditionExpressions.html) in the Developer Guide.

Let's say we want to update the Forum item for DynamoDB to note that there are 5 messages how instead of 4, we only want that change to execute if no other processing thread has updated the item first. This allows us to create idempotent modifications. For more information on idempotent changes please see [Working With Items](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/WorkingWithItems.html#WorkingWithItems.ConditionalUpdate) in the Developer Guide.

To do this from the CLI, we would run:

```bash
aws dynamodb update-item \
    --table-name Forum \
    --key '{
        "Name" : {"S": "Amazon DynamoDB"}
    }' \
    --update-expression "SET Messages = :newMessages" \
    --condition-expression "Messages = :oldMessages" \
    --expression-attribute-values '{
        ":oldMessages" : {"N": "4"},
        ":newMessages" : {"N": "5"}
    }' \
    --return-consumed-capacity TOTAL
```

Note that if you run this exact same command again you will see this error:

```text
An error occurred (ConditionalCheckFailedException) when calling the UpdateItem operation: The conditional request failed
```

Because the *Messages* attribute had already been incremented to *5* in the previous `update-item` call, the second request fails with a *ConditionalCheckFailedException*.

## Exercise

Update the ProductCatalog item where Id=201 to add new colors "Blue" and "Yellow" to the list of colors for that bike type.  Then use the API to remove those "Blue" and "Yellow" list entries to return it to the original state.

Hint: The [Update Expressions](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Expressions.UpdateExpressions.html) page in the Developer Guide has sections on Appending and Removing Elements in a List.

The solution is expandable below but try to figure it out yourself before moving forward.

**Click below to expand and see the exercise solutions**

::::expand{header="Expand this to see the solution"}

First we need to see what the item looks like:

```bash
aws dynamodb get-item \
    --table-name ProductCatalog \
    --key '{"Id":{"N":"201"}}'
```

```json
{
    "Item": {
        "Title": {
            "S": "18-Bike-201"
        },
        "Price": {
            "N": "100"
        },
        "Brand": {
            "S": "Mountain A"
        },
        "Description": {
            "S": "201 Description"
        },
        "Color": {
            "L": [
                {
                    "S": "Red"
                },
                {
                    "S": "Black"
                }
            ]
        },
        "ProductCategory": {
            "S": "Bicycle"
        },
        "Id": {
            "N": "201"
        },
        "BicycleType": {
            "S": "Road"
        }
    }
}
```

We can see that there is a List attribute called *Color* and that it has two colors already, Red and Black.  We will use the *list_append()* function in the UpdateExpression to add the color Blue.

```bash
aws dynamodb update-item \
    --table-name ProductCatalog \
    --key '{
        "Id" : {"N": "201"}
    }' \
    --update-expression "SET #Color = list_append(Color, :values)" \
    --expression-attribute-values '{
        ":values" : {"L": [{"S" : "Blue"}, {"S" : "Yellow"}]}
    }' \
    --return-values ALL_NEW \
    --return-consumed-capacity TOTAL
```

Now when we want to remove those two color entries, we have to reference the index number in the list. DynamoDB lists are 0-based, which means the 3rd and 4th elements we just added are list indexes 2 and 3.  To remove them, we can use this command:

```bash
aws dynamodb update-item \
    --table-name ProductCatalog \
    --key '{
        "Id" : {"N": "201"}
    }' \
    --update-expression "REMOVE Color[2], Color[3]" \
    --return-values ALL_NEW \
    --return-consumed-capacity TOTAL
```

You can use the `get-item` command to verify that these changes were made after each step.
::::
