---
title: "LSQL: Relational Migration to DynamoDB"
weight: 35
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


## Workshop overview

The workshop provides a MySQL instance running on EC2, a Cloud9 developer workstation,
and an S3 bucket for staging data.

You will create a serverless API and Python Lambda function that
performs database read and write operations against the relational database, 
and then deploy a new version that performs read and write operations against DynamoDB.

A sample web app is provided that:
* Acts as a GUI test harness for the serverless API
* Converts tables and indexes into suggested DynamoDB tables and GSIs
* Has a SQL editor with a set of sample queries, and hints on how to combine tables
* Performs read and write operations to both MySQL and DynamoDB
and provides hints and suggestions for building a migration

You will run a set of scripts that:
* Deploys a set of sample MySQL tables, views, and data.
* Converts MySQL table metadata to a DynamoDB table definition.
* Converts the results of a SQL query into DynamoDB JSON format, and stores in the Amazon S3 bucket.
* Perform a full migration by running a SQL query, transforming results to DynamoDB JSON, writing to Amazon S3, then starting a DynamoDB Import job.

Developer challenge: Run the provided SQL samples showing data modeling techniques, 
then apply them to create a new VIEW and use this to perform a custom import.

Developer challenge: Write a new set of data access functions that point to DynamoDB.
 
### Runtime environment
This workshop is designed to run in an AWS-provided environment that includes a MySQL database on EC2.

### Technical Depth
This workshop is a L300 level workshop. Having SQL, Python, and Bash skills will help but are not required.
### Code Project
Attendees will use scripts and tools from the /workshops/relational-migration folder of the
[github.com/aws-samples/aws-dynamodb-examples](https://github.com/aws-samples/aws-dynamodb-examples/) repository.
