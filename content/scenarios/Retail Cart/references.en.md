+++
title = "Retail Cart References"
chapter = false
weight = 1
+++


## How to tackle the challenge...

What are the access patterns?

The access patterns in the scenario are outlined as:

1. Insert and update items placed in a cart by users.
2. Return items related to a user (*AccountID*), sorted by *CreateTimestamp*, and scoped to specific *Status*.
3. Return items across user by *ItemSKU*, sorted by *CreateTimestamp*, and scoped to a specific *Status*.
4. Offline ad hoc queries for BI team.

Identify possible partitions keys to fulfill the primary access pattern:

- What item attribute scales in volume along with higher access?
- What is a natural organization for the related data items? (so as to return collected items relative to the access patterns above)
- Consider the dimension of access: both reads and writes.

How to organize items related to the primary access pattern:

- What organization needs to be written to return items in sorted order? (sort by ?)
- What is hierarchy of the relationships? (most general to more specific)

Fulfilling the second and third access patterns:

- The second access pattern is an OLTP access pattern and can be modeled directly in DynamoDB
- The third access pattern is OLAP and does not need to be fulfilled directly on DynamoDB

Given the above, see below for some helpful references:
**[Using Sort Keys to Organize Data](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-sort-keys.html)**
**[Working with Queries](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Query.html)**
**[Using GSIs to Fulfill Secondary Access Patterns](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GSI.html)**
**[Perform Analytics by using DynamoDB Streams and Amazon Athena](https://aws.amazon.com/blogs/database/how-to-perform-advanced-analytics-and-build-visualizations-of-your-amazon-dynamodb-data-by-using-amazon-athena/)**
