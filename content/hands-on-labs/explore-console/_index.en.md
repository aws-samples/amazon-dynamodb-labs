---
title: "Explore the DynamoDB Console"
menuTitle: "Explore the DynamoDB Console"
date: 2021-04-25T07:33:04-05:00
weight: 30
chapter: true
pre: "<b>3. </b>"

---

In this lab we will be exploring the [DynamoDB section of the AWS Management Console](https://console.aws.amazon.com/dynamodbv2/).  There are two versions of the console and while you can always click "Revert to the current console" we will be working with V2 of the console.

The highest level of abstraction in DynamoDB is a *Table* (there isn't a concept of a "Database" that has a bunch of tables inside of it like in other NOSQL or RDBMS services).  Inside of a Table you will insert *Items*, which are analogous to what you might think of as a row in other services.  Items are a collection of *Attributes*, which are analogous to columns.  Every item must have a *Primary Key* which will uniquely identify that row (two items may not contain the same Primary Key).  At a minimum when you create a table you must choose an attribute to be the *Partition Key* (aka the Hash Key) and you can optionally specify another attribute to be the *Sort Key*.  

If your table is a Partition Key only table, then the Partition Key is the *Primary Key* and must uniquely identify each item.  If your table has both a Partition Key and Sort Key, then it is possible to have multiple items that have the same Partition Key, but the combination of the Partition Key and Sort Key will be the Primary Key and uniquely identify the row.  In other words, you can have multiple items that have the same Partition Key as long as their Sort Keys are different. Items with the same Partition Key are said to belong to the same *Item Collection*.

For more information please read about [Core Concepts in DynamoDB](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.CoreComponents.html).

Operations in DynamoDB consume capacity from the table.  When the table is using On-Demand capacity, read operations will consume *Read Request Units (RRUs)* and write operations will consume *Write Request Units (WRUs)*. When the table is using Provisioned Capacity, read operations will consume *Read Capacity Units (RCUs)* and write operations will consume *Write Capacity Units (WCUs)*.  For more information please see the [Read/Write Capacity Mode](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.ReadWriteCapacityMode.html) in the DynamoDB Developer Guide.

Now lets dive into the shell and explore the DynamoDB Console.
