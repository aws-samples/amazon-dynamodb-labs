+++
title = "Deleting Data"
date = 2020-04-23T07:38:58-05:00
weight = 25
+++

The DynamoDB [DeleteItem API](https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_DeleteItem.html) is used to delete an item.  It is invoked using the [delete-item CLI command](https://docs.aws.amazon.com/cli/latest/reference/dynamodb/delete-item.html).

Deletes in DynamoDB are always singleton operations.  There is no single command you can run that would delete all the rows in the table for example.

Remember that item we added to the **Reply** table in the previous path:

```bash
aws dynamodb get-item \
    --table-name Reply \
    --key '{
        "Id" : {"S": "Amazon DynamoDB#DynamoDB Thread 2"},
        "ReplyDateTime" : {"S": "2021-04-27T17:47:30Z"}
    }'
```

Let's delete this item.  When using the `delete-item` command we need to reference the full Primary Key just like we do with `get-item`:

```bash
aws dynamodb delete-item \
    --table-name Reply \
    --key '{
        "Id" : {"S": "Amazon DynamoDB#DynamoDB Thread 2"},
        "ReplyDateTime" : {"S": "2021-04-27T17:47:30Z"}
    }'
```

It's safe to delete the same item more than once.  You can run the same command above as many times as you want and it won't report an error; if the key doesn't exist then the DeleteItem API still returns success.

Now that we've removed that item from the **Reply** table we also need to decrement the related **Forum** *Messages* count.

```bash
aws dynamodb update-item \
    --table-name Forum \
    --key '{
        "Name" : {"S": "Amazon DynamoDB"}
    }' \
    --update-expression "SET Messages = :newMessages" \
    --condition-expression "Messages = :oldMessages" \
    --expression-attribute-values '{
        ":oldMessages" : {"N": "5"},
        ":newMessages" : {"N": "4"}
    }' \
    --return-consumed-capacity TOTAL
```
