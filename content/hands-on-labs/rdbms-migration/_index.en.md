+++
title = "RDBMS Migration"
menuTitle = "RDBMS Migration"
date = 2021-04-25T07:33:04-05:00
weight = 50
pre = "<b>5. </b>"

+++

Sometimes data appears to be a relational by nature, though the evolving business requirement causes schema disruption over period of time.
Amazon DynamoDB helps IT to rethink the datamodel in a key-value format. Data in the key-value format has potential to absorb the disruption occurs due to schema change caused bu evolving requirement.
Amazon DynamoDB offers fully managed, serverless datastore for information stored in key-value format with single digit milli-second latency at scale.

This excercise will briefly discuss the technique to migrate relational dataset from MySQL to Amazon DynamoDB. The data from the MySQL database is denormalized to create 360 view of an entity before migration.
Multiple tables can be denormalized based on their relationship befor migrating to Amazon DynamoDB. Data Denormalization is a common practice used in NoSQL data modelling to reduce overhead of joins during Query operation.

![Final Deployment Architecture](/images/denormalization.png)
