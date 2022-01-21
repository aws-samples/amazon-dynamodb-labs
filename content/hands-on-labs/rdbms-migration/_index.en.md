+++
title = "Relational Modeling & Migration"
menuTitle = "Relational Modeling & Migration"
date = 2021-04-25T07:33:04-05:00
weight = 50
pre = "<b>5. </b>"

+++

In this module, you will learn how to design target data model in DynamoDB for a highly normalized relational data in relational database.
The exercise also guides a step by step migration of an IMDb dataset from a self-managed MySQL database instance on EC2 to a fully managed key-value pair database Amazon DynamoDB.
At the end of this lesson, you should feel confident in your ability to design and migrate an existing relational database to Amazon DynamoDB.

Sometimes data appears to be in a relational format at given point of time, though the evolving business requirement causes schema changes over the project lifecycle.
Every schema change is labor-intensive, costly and sometimes causes business to reprioritize their needs due to complicated cascading impact.
Amazon DynamoDB helps IT to rethink the data model in a key-value format. Data in the key-value format has the potential to absorb the disruption due to evolving schema caused by changing requirements.
Amazon DynamoDB offers a fully managed, serverless datastore for information stored in key-value format.
Schema flexibility lets DynamoDB store complex hierarchical data within an item and offers single-digit millisecond latency at scale.

This module will briefly discuss the techniques to design target data model and migrate relational datasets from MySQL to Amazon DynamoDB. The IMDb data inside MySQL database is normalized across multiple tables.
We will use denormalized/item collection modelling techniques to create comprehensive data model for identified access patterns.
There are multiple factors that will influence our decision to build target data model
  - Access patterns
  - Cardinality
  - Overall I/O

We will briefly discuss the key aspects to create a model that will serve various access patters with ultralow latency and lower I/O and cost.

![Final Deployment Architecture](/images/denormalization.png)
