---
title: "Find open games"
menuTitle: "Find open games"
date: 2021-04-21T07:33:04-05:00
weight: 40
chapter: true
pre: "<b>4. </b>"
description: "In this module, you learn about using Global Secondary Indexes (GSIs) as a sparse index and use it to find open games."
---

One of the biggest adjustments for users who are new to DynamoDB and NoSQL is how to model data to filter across an entire dataset. For example, in the gaming application, you need to find games with open spots so that you can show users which games they can join.

In a relational database, you would write some SQL to query the data.

```sql
SELECT * 
FROM games 
WHERE status = “OPEN”
```

DynamoDB can [filter results](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Query.html#Query.FilterExpression) on a `Query` or `Scan` operation, but DynamoDB doesn’t work like a relational database. A DynamoDB filter applies **after** the initial items that match the `Query` or `Scan` operation have been retrieved. The filter reduces the size of the payload sent from the DynamoDB service, but the number of items retrieved initially is subject to the [DynamoDB size limits](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Limits.html#limits-api).

Fortunately, there are a number of ways you can allow filtered queries against your dataset in DynamoDB. To provide efficient filters on your DynamoDB table, you need to plan the filters into your table’s data model from the beginning. Remember the lesson you learned in the earlier modules of this lab: Consider your access patterns, and then design your table.

In the next steps, you use a global secondary index to find open games. Specifically, you will use the [sparse index](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-indexes-general-sparse-indexes.html) technique to handle this access pattern.
