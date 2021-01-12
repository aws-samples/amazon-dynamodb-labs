+++
title = "Adjacency Lists"
date = 2020-04-07T10:18:07-08:00
weight = 8
chapter = true
pre = "<b>Exercise 7: </b>"
description = "Learn how to store multiple entity types in one DynamoDB table."
+++

When different entities of an application have a [many-to-many relationship](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-adjacency-graphs.html) between them, it is easier to model the relationship as an adjacency list. In this model, all top-level entities (synonymous with nodes in the graph model) are represented as the partition key. Any relationship with other entities (edges in a graph) are represented as an item within the partition by setting the value of the sort key to the target entity ID (target node).

This example uses an `InvoiceAndBills` table to demonstrate this design pattern. In this scenario, a customer can have multiple invoices, so there is a 1-to-many relationship between a customer ID and an invoice ID. An invoice contains many bills, and a bill can be broken up and associated with multiple invoices. So there is a many-to-many relationship between invoice ID and bill ID. The partition key attribute is either an invoice ID, bill ID, or customer ID.

You will model the table to execute the following queries:
- Using the invoice ID, retrieve the top-level invoice details, customer, and associated bill details.
- Retrieve all invoice IDs for a customer.
- Using the bill ID, retrieve the top-level bill details and the associated invoice details.


#### Table: `InvoiceAndBills`
- Key schema: HASH, RANGE (partition and sort key)
- Table read capacity units (RCUs) = 100
- Table write capacity units (WCUS) = 100
- Global secondary index (GSI):
	- GSI_1 (100 RCUs, 100 WCUs) - Allows for reverse lookup to the related entity.


| Attribute Name (Type)        | Special Attribute?           | Attribute Use Case          | Sample Attribute Value  |
| ------------- |:-------------:|:-------------:| -----:|
| PK (STRING)      | Partition key | Holds the ID of the entity, either a bill, invoice, or customer  | *B#3392* or *I#506* or *C#1317*  |
| SK (STRING)      | Sort key, GSI_1 partition key | Holds the related ID: either a bill, invoice, or customer  | *I#1721* or *C#506* or *I#1317*  |
