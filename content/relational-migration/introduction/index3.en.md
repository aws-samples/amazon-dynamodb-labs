---
title : "Scope and Downtime"
weight : 12
---

## Migration Scope

A large relational database application may span a hundred or more tables and support several 
different application functions. When approaching a large migration, consider breaking your 
application into smaller components or microservices, and migrating a small set of tables at a time. 
This workshop involves migrating only a few tables to support a particular application function.

---

## Offline Migration
If your application can tolerate some downtime during the migration, it will simplify the migration process.
You can keep the relational application in read-only mode to allow for partial availability during the migration window.

* *In this workshop, we will focus on Offline Migrations.*
* *We will use the **DynamoDB Import from S3** feature to populate new tables from staged data.*

## Hybrid Migration
You might allow users to perform both reads and inserts, but not updates and deletes, during a migration.
The application could be modified to perform dual-writes to both the relational and DynamoDB database, 
while a separate job performs a backfill of all historical records into DynamoDB.

## Online Migration
Applications that require zero downtime during migration are more difficult migrate, 
and can require significant planning and custom development. 
One key decision is to estimate and weigh the costs of building a custom migration process 
versus the cost to the business of having a downtime window during the cutover.
