---
title : "Generate Table Definition with Indexes"
weight : 23
---

## Look for indexes on the table

Within the Web App, notice the two Access Pattern tabs near the top of the page.
Click on the second tab called **Querying**

You will now see a form listing the Primary Key index, along with other secondary indexes. 

![Customers Table With Indexes Form](/static/images/relational-migration/customers_indexes_ddb_form.png)


## Convert Table to DynamoDB Table Definition
Now, click on the Generate button below the form. You should see a new version of the DynamoDB 
table definition, this time with one Global Secondary Index (GSI) for each relational table index.

The GSI is a separate data structure that stores your table's data organized by a different primary key,
and can be used to perform efficient queries against a large table.

![Customers Table With Indexes](/static/images/relational-migration/customers_indexes_ddb.png)

Notice that a few more attribute (column) names are defined. Any attributes that are involved in a GSI 
definition need to be declared in advance.


