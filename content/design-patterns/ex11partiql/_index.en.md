+++
title = "Amazon DynamoDB PartiQL"
date = 2019-12-02T10:18:15-08:00
weight = 9
chapter = true
pre = "<b>Exercise 8: </b>"
description = "Learn how to use PartiQL in Amazon DynamoDB."
+++

Amazon DynamoDB supports PartiQL, a SQL-compatible query language, to select, insert, update, and delete data in Amazon DynamoDB.

This section shows how to use PartiQL for DynamoDB from the Amazon DynamoDB console, and the AWS Command Line Interface (AWS CLI).

Following statements are supported in PartiQL for DynamoDB:

- Select

- Update

- Insert

- Delete

Transactions and Batch Operations are also supported.

This example uses an `Gamers` table to demonstrate PartiQL. You will run data manipulation statements - insert, update, delete using PartiQL, use Transactions and conclude with batch operation.
