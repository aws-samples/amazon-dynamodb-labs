---
title : "Project Requirements"
weight : 21
---

## Plan a migration to DynamoDB
The business has evaluated DynamoDB and likes the features and performance it offers.
Our mission is to manage a project to assess, plan, and build a migration of the existing 
Sales Orders application from the relational database onto DynamoDB.

### Explore approaches

We have been given time to explore different potential approaches to the migration.

A goal of the project is to learn how to migrate tables using DynamoDB's Single Table pattern,
while planning an alternate, traditional 1-for-1 table migration in case it seems to be a better approach.

### Leverage skills of IT staff

We have been asked to write any data transformation logic in SQL, so the existing IT Database staff
will feel comfortable performing future migrations. 

The existing application code is modular, so that operations like
"list products", "get customer" and "delete order line" are defined and encapsulated
in data access functions within the Python code base.
This should make it somewhat easy to find these read and write functions and then
swap out the SQL operations for DynamoDB API calls. If we do it right, the bulk of the application
code will not need to be changed. 

But, we can't begin to make these changes until we have
all agreed on what the new DynamoDB table schema and data formats will look like.


