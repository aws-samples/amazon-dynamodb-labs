---
title: "Relational Migration to DynamoDB"
weight: 0
---

![Relational Migration](/static/images/relational-migration/frontpage.png)

Developers are choosing to migrate relational database applications to DynamoDB
to take advantage of DynamoDB's serverless scalable architecture,
predictable low latency performance, high availability and durability, and low maintenance.

However, migrating a relational database application like MySQL onto a NoSQL database like Amazon DynamoDB 
requires careful planning to achieve a successful outcome.

This workshop will give you hands-on experience and tools to evaluate existing relational tables, 
define logic to transform and shape relational data, 
and build migration jobs to extract, stage, and load data into DynamoDB. 

A reference application is provided that reads and writes to a relational database. 
A new version of the app that uses DynamoDB instead is included, 
to highlight the code updates required to use the DynamoDB API.


### Relational Migration to DynamoDB Guide
A robust set of documentation has been published on strategies for migrating relational databases to DynamoDB, 
which can be found at the link below. This workshop compliments the guide and provides hand-on practice implementing 
many of the approaches discussed within. 
You can review this guidance when considering and planning your own relational migration to DynamoDB. 

[AWS Documentation: Relational Migration to DynamoDB Developer Guide](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/migration-guide.html)

[//]: # (## Workshop overview)

[//]: # (The workshop includes a Cloud9 developer workstation and an S3 bucket for staging data.)

[//]: # (The source database for migration is a deployed a MySQL instance, running on EC2. )

[//]: # (Run a script to deploy the sample set of MySQL tables and data.)

[//]: # (You will create a serverless API and Python Lambda function that)

[//]: # (performs database read and write operations against the relational database. )

[//]: # (A sample web app provides a GUI interface as a test harness for the serverless API. )

[//]: # ()
[//]: # (An end-to-end migration script is run that performs a SQL query, transforms results to DynamoDB JSON and writes to Amazon S3, then starts a DynamoDB Import job.)

[//]: # ()
[//]: # (Developer challenge: Tour various SQL data modeling techniques, then combine them into a final single-table transformation. )

[//]: # (Developer challenge: write a new set of data access functions that point to DynamoDB. )

[//]: # ()



 

