---
title : "Schema Refactoring"
weight : 22
---

## Discovering Table columns, data types, and indexes

As consultants, we need to do some discovery and scoping to define what our starting parameters are
for the migration. In particular, we want to find out all we can about existing tables including their:
* Columns and data types
* Primary Key column(s)
* Indexes
* Constraints

In MySQL, a system schema called INFORMATION_SCHEMA holds the answers to these questions. We could query
this schema and learn what currently exists. We could also use the standard MySQL Workbench tool to do the same.
However, what would be even better would be to get suggestions for how to convert the table metadata
to DynamoDB format. The Chalice API and Web App are designed to help us with this.

