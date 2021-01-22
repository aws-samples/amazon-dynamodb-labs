+++
title = "Step 3 - Performing Transactions with PartiQL for DynamoDB"
date = 2019-12-02T12:24:33-08:00
weight = 1
+++

### Performing Transactions with PartiQL for DynamoDB

Transactions in DynamoDB can be used to make coordinated, all-or-nothing changes to multiple items both within and across tables.

You can group multiple Insert, Update, and Delete statements as part of Transaction. But the transaction must consist of either read statements or write statements; you cannot mix both in one transaction.

We will use transaction to bump up Health and decrement Coins for Gamer - `Atom12` as all or nothing operation. Also, we will add `conditioncheck` to check if Gamer has enough coins.

We have written following transaction block to meet this requirement.

```
[
    {
        "Statement": "update Gamers set Health = '100%' where PK='Atom12' and SK='Status'"
    },
    {
        "Statement": "update Gamers set Coins=Coins - 400 where PK='Atom12' and SK='Assets' and Coins > 400"
    }
]
```
Now, execute this statement.

`aws dynamodb execute-transaction --transact-statements  file://partiql_transactions.json`

We can view the changes in Coins and Health attributes using `select` statement. Let's run below `select` statement. This time from CLI instead of PartiQL editor.

`aws dynamodb execute-statement --statement "select * from Gamers where PK='Atom12'"`

Try running `execute-transaction` statement again. Conditioncheck should fail as number of Coins for this item is now less than 400.
