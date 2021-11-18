+++
title = "RDBMS Migration"
menuTitle = "RDBMS Migration"
date = 2021-04-25T07:33:04-05:00
weight = 50
pre = "<b>5. </b>"

+++

In this lesson, you migrate a self-managed MySQL database instance to a fully managed database key-value pair database Amazon DynamoDB.
First, you learn why you would want to use DynamoDB to manage your relational database.
Then, you work through the steps to migrate an existing MySQL database to Amazon DynamoDB.
At the end of this lesson, you should feel confident in your ability to migrate an existing relational database to Amazon DynamoDB.

Sometimes data appears to be relational by nature at any point in time, though the evolving business requirement causes schema disruption over a period of time.
Amazon DynamoDB helps IT to rethink the data model in a key-value format. Data in the key-value format has the potential to absorb the disruption that occurs due to schema change caused by evolving requirements.
Amazon DynamoDB offers a fully managed, serverless datastore for information stored in key-value format with single-digit millisecond latency at scale.

This exercise will briefly discuss the technique to migrate relational datasets from MySQL to Amazon DynamoDB. The data from the MySQL database is denormalized to create a 360 view of an entity before migration.
Multiple tables can be denormalized based on their relationship before migrating to Amazon DynamoDB. Data Denormalization is a common practice used in NoSQL data modeling to reduce the overhead of joins during Query operation.

![Final Deployment Architecture](/images/denormalization.png)
