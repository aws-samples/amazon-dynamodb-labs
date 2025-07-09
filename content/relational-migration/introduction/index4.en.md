---
title : "How Much Transformation is needed?"
weight : 13
---

### Could you just migrate existing tables as they are, one-for-one?

![One for One table migration](/static/images/relational-migration/oneforone.png)

Consider the question in this section header. Is this even a good idea? This question generates a great deal of debate and interest in the data modeling community.

The DynamoDB **single table philosophy** is to store different types of records together in a single table in DynamoDB.

Here are some pros and cons of migrating relational tables directly into DynamoDB tables.


| Schema Transformation Option                                                                                                                               | Benefits / Drawbacks                                                                                                                                            |
|------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------| 
| Copy tables 1-for-1 directly into DynamoDB                                                                                                                 | Easier to migrate<br/>Harder in DynamoDB to fetch related data from multiple tables                                                                             |
| Transform Schema for NoSQL: <br/>&nbsp;&nbsp;&nbsp;&nbsp;Denormalized<br/>&nbsp;&nbsp;&nbsp;&nbsp;Single-Table<br/>&nbsp;&nbsp;&nbsp;&nbsp;Item Collecions | Easier to keep related data together for low-latency reads<br/>Harder to update any duplicated, denormalized data<br/>Harder to achieve zero-downtime migration |


## Combining tables using a SQL VIEW

You could use a SQL VIEW to perform a custom transformation of data from multiple tables. 
The view will need the leading one or two columns to provide a unique primary key, to identify each row.
The SQL language provides several powerful features you can use to combine, reshape, format, calculate source data
into a custom dataset ready for import to DynamoDB, which we will explore in this workshop.

![Single Table Transformation with VIEW](/static/images/relational-migration/singletableview.png)




