+++
title = "Bank Payments References"
chapter = false
weight = 1
+++

## How to tackle this challenge

**What are the access patterns?**

The access patterns in the scenario are outlined as:

1. Insert scheduled payments.
2. Return scheduled payments by user for the next 90 days.
3. Return payments across users for specific date by status (`SCHEDULED` or `PENDING`).  

Identify possible partitions keys to fulfill the primary access pattern:

- What item attribute (*AccountID*, *ScheduledDate*, *Status*, *DataBlob*) scales with access patterns?
- What is a natural organization for the related payment items (so as to return collected items relative to the access patterns above)?
- Consider the dimension of access: both reads and writes.

When determining how to organize items related to the primary access pattern:

- What organization do items need to be written with to return items by user for a date range (sort by)?
- What is the hierarchy of the relationships and when does it apply (most general to more specific)?

Fulfilling the third access patterns:

- The third access pattern is OLTP and can be fulfilled directly on DynamoDB



#### Helpful references

Given the above, see below for some helpful references.
- **[Best Practices for Using Sort Keys to Organize Data](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-sort-keys.html)**
- **[Working with Queries](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Query.html)**
- **[Using Global Secondary Indexes in DynamoDB](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GSI.html)**
- **[Write Shard a GSI for Selective Queries in DynamoDB](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-indexes-gsi-sharding.html)**
