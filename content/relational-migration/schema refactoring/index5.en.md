---
title : "Single Table Philosophy"
weight : 27
---

### Schema Consolidation for Single Table
Without any JOIN operator to combine data from multiple tables, developers often store different types 
of records all in the same table in DynamoDB. This allows for item collections to emerge. 
Item collections are sets of records that have something in common, are stored together, 
and can be retrieved quickly and efficiently with 
a query operation. A great and thorough overview of Single Table Philosophy is covered in this 
[blog post](https://aws.amazon.com/blogs/database/single-table-vs-multi-table-design-in-amazon-dynamodb/).

Let's assume we wish to combine the Customers and Orders table together with a JOIN to produce a single data set.
The database schema includes constraints that hint at how tables should be combined with a JOIN.

### Foreign Key constraints as hints

1. From the web app left nav, click on the Orders table. 
2. Click on the Querying tab near the top of the page.
3. Scroll to the bottom of the page and find the button labeled Foreign Key Relationships

![Foreign Key Relationship](/static/images/relational-migration/foreign_key.png)

4. Click the "Paste to editor" button to put a sample query into the SQL box.
   ::alert[The SQL editor window allows you to build and test SQL queries. Look for query results in a grid at the bottom of the page.]
5. Press the **Run SQL** button to see the results of the query. 

Notice that the leading columns are just the first columns in the Orders table.

![Foreign Query Result](/static/images/relational-migration/fk_result.png)

For this workshop, we prefer to have the first column of any dataset represent the new table's Partition Key.
And the second column should be the new table's Sort Key (if a Sort Key is needed).

A SQL View has been created for you that performs the JOIN but instead returns the first two columns as cust_id and ord_id.
This aligns nicely with a DynamoDB table's two-part primary key. The Partition Key representing a customer can have 
one or more records, each with a unique Sort Key value representing an order.

6. Just below the SQL editor panel, find the button called **vCustOrders** and click it.
7. Review the result data set and notice that cust_id and ord_id are in the leading positions now.

   ![VIEW Result](/static/images/relational-migration/view_result.png)

If you wish to check the VIEW definition, open the file ```source-tables/create_views.sql```

Now, let's generate a DynamoDB table definition based on this view's output. 

8. Run: 
```bash
python mysql_desc_ddb.py vCustOrders 
```

The script returns a new table definition based on the name of the view, with the first 
column becoming the Partition Key. The script will assume data types of string (S) by default.

However, cust_id is not unique across the dataset. We want to get a table definition that uses the 
first TWO column names as the Partition Key and Sort Key.

9. Run:
```bash
python mysql_desc_ddb.py vCustOrders 2
```
Now we can see that the DynamoDB table's Key Schema includes both columns.

#### Custom GSIs 
Unlike the previous table definition we generated, this one will have no GSIs defined since there are no
indexes on a relational VIEW. If you need a GSI, you can manually add it to the table definition, or else 
you can request a new GSI at any time on an existing DynamoDB table. 

### Summary
We learned how to generate a full table definition from an existing table, 
or a simplified table definition from the leading columns of a VIEW that combines records from multiple tables.

Next up is the Data Migration section of the workshop.

