+++
title = "Join and close games"
menuTitle = "Join and close games"
date = 2021-04-21T07:33:04-05:00
weight = 50
chapter = true
pre = "<b>5. </b>"
description = "In this module, you learn about DynamoDB transactions and you use a DynamoDB transaction when adding new users to a game while preventing the game from becoming overloaded."
+++

Through the earlier modules in this lab, you have satisfied the access patterns for the creation and retrieval of core entities in the gaming application, such as `Users` and `Games`. You also used a sparse GSI to find open games that users can join.

In this module, you satisfy two access patterns:

- Join game for a user (Write)
- Start game (Write)


Note that both of these access patterns are writing data to DynamoDB, in contrast to the read-heavy patterns you have done so far in this lab.

## DynamoDB transactions

To satisfy the “Join game for a user” access pattern in this module’s steps, you are going to use [DynamoDB transactions](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/transactions.html). Transactions are popular in relational systems for operations that affect multiple data elements at once. For example, imagine you are running a bank. One customer transfers $100 to another customer. When recording this transaction, you would use a transaction to make sure the changes are applied to the balances of both customers rather than just one.

DynamoDB transactions make it easier to build applications that alter multiple items as part of a single operation. With transactions, you can operate on up to 100 items as part of a single transaction request. In a [TransactWriteItems](https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_TransactWriteItems.html) API call, you can use the following operations:

- **Put**: For inserting or overwriting an item.
- **Update**: For updating an existing item.
- **Delete**: For removing an item.
- **ConditionCheck**: For asserting a condition on an existing item without altering the item.


In the following steps, you use a DynamoDB transaction when adding new users to a game while preventing the game from becoming overfilled.
