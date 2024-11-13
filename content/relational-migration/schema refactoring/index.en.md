---
title : "Schema Refactoring"
weight : 20
---

## Business Scenario - Vehicle Sales

![Vehicles Photo](/static/images/relational-migration/vehicles.png)

Let's review the sample tables provided by the workshop. 

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


## Plan a migration to DynamoDB
The business has evaluated DynamoDB and likes the features and performance it offers.
We have been asked to manage a migration of the existing Sales Orders application from the
relational database onto DynamoDB.


We have been given time to explore different potential approaches to the migration.
Our application code is modular, so that operations like "list products", "get customer" and "delete order line"
are all defined and encapsulated in data access functions within our code.
This should make it somewhat easy to find these read and write functions and then
swap out the SQL operations for DynamoDB API calls. If we do it right, the bulk of the application
code will not need to be changed. But, we can't begin to make these changes until we have
all agreed on what the new DynamoDB table schema and data formats will look like.