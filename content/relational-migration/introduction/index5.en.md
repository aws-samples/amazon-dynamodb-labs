---
title : "Transform, Extract, Convert, Stage, Import"
weight : 14
---

## Staging Data for DynamoDB Import 


![Extract](/static/images/relational-migration/extract.png)

Once the data is fully staged in S3, we can then request a
[DynamoDB Import from S3](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/S3DataImport.HowItWorks.html),
which will create a new table and load the S3 data for us. 
This import is fully managed by DynamoDB, saving us the trouble of creating and running a data load job, 
and is priced to be much less expensive than the cost of consuming DynamoDB WCU units directly in a load job.


The Import from S3 feature requires a table definition for the new table to be created.
The table definition includes details about the table including:
* Table Name
* Partition Key name and type
* Sort Key name and type (optional)
* Global Secondary Index (GSI) definitions (optional)

[Global secondary indexes](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GSI.html) (GSIs) are optional, but the decision of whether and how to add these indexes to our table is an important one.
Done right, a GSI will unlock efficient new search capabilities on our DynamoDB table, but would increase the cost
of a write-heavy workload.  We will learn how to automate or customize the index definitions created
during the Import process. 

![Import from S3](/static/images/relational-migration/import.png)
