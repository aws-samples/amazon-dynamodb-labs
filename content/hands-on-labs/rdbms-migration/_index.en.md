+++
title = "Relational Modeling & Migration"
menuTitle = "Relational Modeling & Migration"
date = 2021-04-25T07:33:04-05:00
weight = 50
pre = "<b>5. </b>"

+++

In this module, you will learn how to design a target data model in DynamoDB for highly normalized relational data in a relational database.
The exercise also guides a step by step migration of an IMDb dataset from a self-managed MySQL database instance on EC2 to a fully managed key-value pair database Amazon DynamoDB.
At the end of this lesson, you should feel confident in your ability to design and migrate an existing relational database to Amazon DynamoDB.

Sometimes data appears to be in a relational format at given point of time, though evolving business requirements cause schema changes over the project lifecycle.
Every schema change is labor-intensive, costly and sometimes causes the business to reprioritize their needs due to complicated cascading impacts.
Amazon DynamoDB helps IT to rethink the data model in a key-value format. Such a format has the potential to absorb disruption caused by an evolving schema.
Amazon DynamoDB offers a fully managed, serverless datastore for information stored in key-value format.
Schema flexibility lets DynamoDB store complex hierarchical data within an item and offers single-digit millisecond latency at scale.

This module will briefly discuss techniques to design a target data model and migrate relational datasets from MySQL to Amazon DynamoDB. IMDb data inside a MySQL database starts out as normalized across multiple tables.
We will use denormalized/item collection modelling techniques to create a comprehensive data model for identified access patterns.
There are multiple factors that will influence our decisions in building the target data model:
  - Access patterns
  - Cardinality
  - Overall I/O

We will briefly discuss the key aspects of creating a model that will serve various access patters with ultralow latency and low I/O and cost.

![Final Deployment Architecture](/images/denormalization.png)
