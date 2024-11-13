---
title : "Introduction"
weight : 10
---

# Motivations for Migrating to DynamoDB

![Rationales](/static/images/relational-migration/rationales.png)

When designing a DynamoDB solution, you will need to make several decisions on 
how best to leverage DynamoDB's unique feature set. These decisions
may involve trade-offs between competing benefits. 
In a classic example, consider a table that has no secondary indexes, 
and consider the same table, but with three different indexes to support 
various search patterns. The first table scores high on the dimensions of 
Low Cost and Simplicity, but may perform poorly if the table is large and 
queries need to perform a full table scan to execute a search.

Another trade off comes with deciding how many tables will be required in 
your DynamoDB schema. Without JOIN operators, you may need to make multiple calls to 
read from separate tables when retrieving data. This table schema may match the 
existing relational schema, greatly simplifying and streamlining the migration process,
but at the expense of more complex and potentially slower read operations. 
With DynamoDB, you can choose to transform existing tables' data into 
single-table or single-item format to bring related data close together, 
adding some complexity to the write process, but also unlocking the ability 
to do fast sub-10 millisecond read operations. 

As you learn the features of DynamoDB and plan your migration, keep the starting
motivations in mind so that you can make the best choices to satisfy your most 
important requirements.

## Additional considerations
To further maximize the benefits of DynamoDB, these metrics should be 
documented for future use.

* What is the maximum write velocity and read velocity (per second) now and in the future?
* For any large, growing tables: How long will records live before they are safe to delete or archive?



[//]: # (## Pre-requisites)

[//]: # (This migration is designed to be run during an AWS-sponsored event,)

[//]: # (where a starting environment is created and provided for you.)

[//]: # (The starting environment includes a running MySQL instance, an S3 bucket, and Cloud9 developer workstation)

[//]: # (for performing the workshop steps.)

[//]: # ()
[//]: # ()
[//]: # (You can also setup and run the migration using your own laptop, )

[//]: # (AWS account, and your existing MySQL database, by updating the file: )

[//]: # ([.chalice/config.json]&#40;https://github.com/aws-samples/aws-dynamodb-examples/blob/master/relational-migration/.chalice/config.json&#41;)

[//]: # ()
[//]: # ()
[//]: # ()
[//]: # (## Workshop Overview)

[//]: # (You will practice a relational migration by identifying existing tables, )

[//]: # (migrating them first one by one into DynamoDB, )

[//]: # (then by creating a custom SQL VIEW that transforms data using SQL expressions.)

[//]: # ()
