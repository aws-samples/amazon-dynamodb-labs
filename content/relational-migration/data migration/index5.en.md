---
title : "SQL Transformation Patterns for DynamoDB"
weight : 34
---

## Shaping Data with SQL

Let's return to the web app and explore some techniques you can use to shape and enrich your relational
data before importing it to DynamoDB.

1. Within the web app, refresh the browser page.
2. Click on the Querying tab.
3. Notice the set of SQL Sample buttons below the SQL editor.
4. Click button one. 
The OrderLines table has a two-part primary key, as is common with DynamoDB. We can think of the returned dataset as an Item Collection.
5. Repeat by clicking each other sample buttons. Check the comment at the top of each query, which summarizes the technique being shown.

![SQL Samples](/static/images/relational-migration/sparse.png)

Notice the final two sample buttons. These demonstrate alternate ways to combine data from multiple tables.
We already saw how to combine tables with a JOIN operator, resulting in a denormalized data set.

The final button shows a different approach to combining tables, without using JOIN. 
You can use a UNION ALL between multiple SQL queries to stack datasets together as one. 
When we arrange table data like this, we describe each source table as an entity and so the single DynamoDB
table will be overloaded with multiple entities. Because of this, we can set the partition key and sort key
names to generic values of PK and SK, and add some decoration to the key values so that it's clear what type
of entity a given record represents.

![Stacked entities](/static/images/relational-migration/stacked.png)