+++
title = "Adjacency Lists"
date = 2019-12-02T10:18:07-08:00
weight = 8
chapter = true
pre = "<b>Exercise 7: </b>"
+++


When different entities of an application have a many-to-many relationship between them, it is easier to model the relationship as an adjacency list. In this model, all top level entities (synonymous to nodes in the graph model) are represented as the partition key (PK). Any relationship with other entities (edges in a graph) are represented as an item within the partition by setting the value of the sort key (SK) to the target entity ID (target node).

We will use the Invoices and Bills example to demonstrate this design pattern. In this application, a customer can have multiple Invoices, so there is a 1-to-many relationship between a Customer ID and an Invoice ID. An Invoice contains many bills, and a bill can be broken up and associated with multiple invoices. So there is a many-to-many relationship between Invoice ID and Bill ID. The partition key (PK) attribute will either be an Invoice ID, Bill ID, or a Customer ID. We will be modeling the table to execute the following queries:

- Using the Invoice ID, retrieve the top-level Invoice details, customer, and the associated Bill details
- Retrieve all Invoice IDs for a Customer
- Using the Bill ID, retrieve the top-level Bill details and the associated Invoice details


#### Table InvoiceAndBills:

- Key schema: HASH, RANGE
- Table RCU = 100
- Table WCU = 100
- GSI(s):
  - GSI_1 (100 RCU, 100 WCU) - *Allows for reverse lookup to the related entity*

| Attribute name (Type)        | Special attribute?           | Attribute use case          | Sample attribute value  |
| ------------- |:-------------:|:-------------:| -----:|
| PK (STRING)      | Hash key, GSI 1 hash key | Holds the id of the entity, either a bill, invoice, or customer  | *B#3392* or *I#506* or *C#1317*  |
| SK (STRING)      | Sort key | Holds the related id: either a bill, invoice, or customer  | *I#1721* or *C#506* or *I#1317*  |
