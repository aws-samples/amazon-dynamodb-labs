+++
title = "Transactions"
date = 2020-04-24T07:38:58-05:00
weight = 26
+++

The DynamoDB [TransactWriteItems API](https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_TransactWriteItems.html) is a synchronous write operation that groups up to 25 action requests (subject to an aggregate 4MB size limit for the transaction). It is invoked using the [transact-write-items CLI command](https://docs.aws.amazon.com/cli/latest/reference/dynamodb/transact-write-items.html).

These actions can target items in different tables, but not in different AWS accounts or Regions, and no two actions can target the same item. The actions are completed atomically so that either all of them succeed, or all of them fail. For a greater discussion on Isolation Levels for Transactions see the [Developer Guide](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/transaction-apis.html#transaction-isolation).

You'll recall from previous modules that the sample data contains multiple related tables: **Forum**, **Thread**, and **Reply**.  When a new **Reply** item is added, we also need to increase the Messages count in the related **Forum** item. This should be done in a transaction so that both changes succeed or both changes fail at the same time, and someone reading this data should see both changes or neither change at the same time.

Transactions in DynamoDB respect the concept of idempotency. Idempotency gives you the ability to send the same transaction more than once, but DynamoDB will only execute that transaction once.  This is especially useful when using APIs that aren't themselves idempotent, like using UpdateItem to increment or decrement a number field for example. When executing a transaction you will specify a string to represent the ClientRequestToken (aka Idempotency Token).  For more discussion of idempotency please see the [Developer Guide](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/transaction-apis.html)

That command in the CLI would be:

```bash
aws dynamodb transact-write-items --client-request-token TRANSACTION1 --transact-items '[
    {
        "Put": {
            "TableName" : "Reply",
            "Item" : {
                "Id" : {"S": "Amazon DynamoDB#DynamoDB Thread 2"},
                "ReplyDateTime" : {"S": "2021-04-27T17:47:30Z"},
                "Message" : {"S": "DynamoDB Thread 2 Reply 3 text"},
                "PostedBy" : {"S": "User C"}
            }
        }
    },
    {
        "Update": {
            "TableName" : "Forum",
            "Key" : {"Name" : {"S": "Amazon DynamoDB"}},
            "UpdateExpression": "ADD Messages :inc",
            "ExpressionAttributeValues" : { ":inc": {"N" : "1"} }
        }
    }
]'
```

Look at the **Forum** item and you'll see that the Messages count was incremented by 1, from 4 to 5.

```bash
aws dynamodb get-item \
    --table-name Forum \
    --key '{"Name" : {"S": "Amazon DynamoDB"}}'
```

```json
...
"Messages": {
    "N": "5"
}
...
```

If you run the same transaction command again, with the same `client-request-token` value, you can verify that the other invocations of the transaction are essentially ignored and the *Messages* attributed remains at **5**.

Now we need to do another transaction to reverse the above operation and clean up the table:

```bash
aws dynamodb transact-write-items --client-request-token TRANSACTION2 --transact-items '[
    {
        "Delete": {
            "TableName" : "Reply",
            "Key" : {
                "Id" : {"S": "Amazon DynamoDB#DynamoDB Thread 2"},
                "ReplyDateTime" : {"S": "2021-04-27T17:47:30Z"}
            }
        }
    },
    {
        "Update": {
            "TableName" : "Forum",
            "Key" : {"Name" : {"S": "Amazon DynamoDB"}},
            "UpdateExpression": "ADD Messages :inc",
            "ExpressionAttributeValues" : { ":inc": {"N" : "-1"} }
        }
    }
]'
```
