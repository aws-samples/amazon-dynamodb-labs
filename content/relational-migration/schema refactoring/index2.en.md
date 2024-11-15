---
title : "Table Survey"
weight : 23
---

## Review a table

Returning to the Web App, click on the Tables button.
You should now see a list of the tables in the database. Click on the Customers table.

![Customers Table](/static/images/relational-migration/customers.png)

The table has columns with VARCHAR, INT, and DATETIME data types. The Primary Key column, cust_id, is indicated in blue.

If we were to move this table's data into DynamoDB, we could convert the VARCHAR types into
DynamoDB String (S) format, and the INT into DynamoDB Number (N) format.
However, DynamoDB does not have a native date format.

Instead, dates are usually written as Strings in ISO 8601 format like this: ```"2025-12-13 09:45:37"```

Dates can also be stored as Numbers. The DynamoDB TTL automatic expiration feature requires future
dates to be stored in Epoch number format like this: ```1731934325```. DynamoDB TTL (Time To Live) is a feature that automatically deletes items from a DynamoDB table after a specified time. For more information see [using time to live](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/TTL.html) in our developer documentation.

## Convert Table to DynamoDB Table Definition

The tool provides a routine to generate a DynamoDB table definition based on the
columns and keys from a given relational table. Click the GENERATE button below the table details.

![Generate Customer Table](/static/images/relational-migration/customers_ddb.png)

This JSON format can be used to create a table with various automation tools,
such as the [AWS CLI](https://docs.aws.amazon.com/cli/)
**[create-table](https://docs.aws.amazon.com/cli/latest/reference/dynamodb/create-table.html)** command.


Notice that there are no details on the last_updated datetime column or any other columns, apart from cust_id.
DynamoDB tables are schema-less, meaning that the developer would indicate the data type
attribute values (columns) only when they write a new record. And, each record could have different attributes,
since the database itself will not enforce any data record convention.




