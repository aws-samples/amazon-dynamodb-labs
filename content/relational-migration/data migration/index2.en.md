---
title : "ETL Scripts"
weight : 31
---


## mysql_s3.py

A script called mysql_s3.py is provided that performs all the work to convert and load a query result
set into S3. We can run this script in preview mode by using the "stdout" parameter.

1. Run:
```bash
python3 mysql_s3.py Customers stdout
```
You should see results in DynamoDB JSON format:

![mysql_s3.py output](/static/images/relational-migration/mysql_s3_output.png)

2. Next, run it for our view:
```bash
python3 mysql_s3.py vCustOrders stdout
```
You should see similar output from the view results.

The script can write these to S3 for us. We just need to omit the "stdout" command line parameter.

3. Now, run the script without preview mode:
```bash
python3 mysql_s3.py Customers 
```
You should see confirmation that objects have been written to S3:

![mysql_s3.py output](/static/images/relational-migration/mysql_s3_write_output.png)


