+++
title = "Best Practices"
menuTitle = "Best Practices"
date = 2021-04-21T07:33:04-05:00
weight = 21
chapter = false
pre = ""
description = "To get started, you configure your environment and download code that you use during the lab."
+++

### Use the following best practices when modeling data with DynamoDB

#### Focus on access patterns

When doing any kind of data modeling, you will start with an entity-relationship diagram that describes the different objects (or entities) in your application and how they are connected (or the relationships between your entities).

In relational databases, you will put your entities directly into tables and specify relationships using [foreign keys](https://en.wikipedia.org/wiki/Foreign_key). After you have defined your data tables, a relational database provides a flexible query language to return data in the shape you need.

In DynamoDB, you think about access patterns before modeling your table. NoSQL databases are focused on speed, not flexibility. You first ask how you will access your data, and then model your data in the shape it will be accessed.

Before designing your DynamoDB table, document every need you have for reading and writing data in your application. Be thorough and think about all the flows in your application because you are going to optimize your table for your access patterns.

#### Optimize for the number of requests to DynamoDB

After you have documented your application’s access pattern needs, you are ready to design your table. You should design your table to minimize the number of requests to DynamoDB for each access pattern. Ideally, each access pattern should require only a single request to DynamoDB, so you want to reduce the number of round trips from the application to the table.

##### To optimize for the number of requests to DynamoDB, you need to understand some core concepts:

- [Primary Keys](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.CoreComponents.html#HowItWorks.CoreComponents.PrimaryKey)

- [Secondary Indexes](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/SecondaryIndexes.html)

- [Transactions](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/transactions.html)

#### Don’t fake a relational model

People new to DynamoDB often try to implement a relational model on top of nonrelational DynamoDB. If you try to do this, you will lose most of the benefits of DynamoDB.

##### The most common anti-patterns (ineffective responses to recurring problems) that people try with DynamoDB are:

**Normalization**

In a relational database, you normalize your data to reduce data redundancy and storage space, and then use joins to combine multiple different tables. However, joins at scale are slow and expensive. DynamoDB does not allow for joins because they slow down as your table grows.

**One entity type per table**

Your DynamoDB table will often include different types of data in a single table. In the example, you have `User`, `Game`, and `UserGameMapping` entities in a single table. In a relational database, this would be modeled as three different tables.

**Too many secondary indexes**

People often try to create a secondary index for each additional access pattern they need. DynamoDB is schemaless, and this applies to your indexes, too. Use the flexibility in your attributes to reuse a single secondary index across multiple data types in your table. This is called [index overloading](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-gsi-overloading.html).



In the next step, we will build the entity-relationship diagram and map out the access patterns up front. These should always be your first steps when using DynamoDB. Then, in the modules that follow, you implement these access patterns in the table design.
