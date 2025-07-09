---
title : "Business Scenario"
weight : 20
---
## Business Scenario - Vehicle Sales

Imagine we are hired as consultants to support the sales order application
for a company that sells a range of vehicles, including cars, motorcycles,
and helicopters.
The vehicle customers are various taxi and transport companies,
who contact one of our sales representatives to place new orders.


## Database Schema
The company tracks five types of records in their MySQL Database.
Each entity is stored in a separate table:

* Customers
* Orders
* OrderLines
* Products
* Reps

Foreign key constraints between these tables define **one-to-many** relationships.
For example:
* Each order is tied to one customer, while one customer might have
  multiple orders.
* Each order line is tied to one order (the order header), while one order might have multiple order line items.

The Entity Relationship Diagram (ERD) for our database schema is as follows:

![Relational Application Schema](/static/images/relational-migration/relational_schema.png)


