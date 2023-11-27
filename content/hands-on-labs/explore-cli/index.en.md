---
title: "2. Explore DynamoDB with the CLI"
date: 2021-04-21T07:33:04-05:00
weight: 20
chapter: true
---

We will be exploring DynamoDB with the AWS CLI using the [AWS cloud9 management Console](https://console.aws.amazon.com/cloud9/home).  If you haven't already, choose *open IDE* to launch AWS Cloud9 environment. You can close the Welcome screen and adjust your terminal to increase screen area, or close all the windows and navigate to *Window* -> *New Terminal* to open a new terminal window.

The highest level of abstraction in DynamoDB is a *Table* (there isn't a concept of a "Database" that has a bunch of tables inside of it like in other NOSQL or RDBMS services).  Inside of a Table you will insert *Items*, which are analogous to what you might think of as a row in other services.  Items are a collection of *Attributes*, which are analogous to columns.  Every item must have a *Primary Key* which will uniquely identify that row (two items may not contain the same Primary Key).  At a minimum when you create a table you must choose an attribute to be the *Partition Key* (aka the Hash Key) and you can optionally specify another attribute to be the *Sort Key*.  

If your table is a Partition Key only table, then the Partition Key is the *Primary Key* and must uniquely identify each item.  If your table has both a Partition Key and Sort Key, then it is possible to have multiple items that have the same Partition Key, but the combination of the Partition Key and Sort Key will be the Primary Key and uniquely identify the row.  In other words, you can have multiple items that have the same Partition Key as long as their Sort Keys are different. Items with the same Partition Key are said to belong to the same *Item Collection*.

For more information please read about [Core Concepts in DynamoDB](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.CoreComponents.html).

Operations in DynamoDB consume capacity from the table.  When the table is using On-Demand capacity, read operations will consume *Read Request Units (RRUs)* and write operations will consume *Write Request Units (WRUs)*. When the table is using Provisioned Capacity, read operations will consume *Read Capacity Units (RCUs)* and write operations will consume *Write Capacity Units (WCUs)*.  For more information please see the [Read/Write Capacity Mode](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.ReadWriteCapacityMode.html) in the DynamoDB Developer Guide.

Now lets dive into the shell and explore DynamoDB with the AWS CLI.
