---
title : "Data Migration"
weight : 30
---

## Transform, Extract, Convert, Stage Import

Recall our strategy for migrating table data into DynamoDB via S3 was 
summarized in the :link[Workshop Introduction]{href="../introduction/index5" target=_blank}.

For each table or view that we want to migrate, we need a routine that will ```SELECT *``` from it, 
and convert the result dataset into DynamoDB JSON before writing it to an S3 bucket.

![Migration Flow](/static/images/relational-migration/migrate_flow.png)

For migrations of very large tables we may choose to use purpose-built data tools like 
AWS Glue, Amazon EMR, or Amazon DMS. These tools can help you define and coordinate multiple 
parallel jobs that perform the work to extract, transform, and stage data into S3.

In this workshop we can use a Python script to demonstrate this ETL process. 
