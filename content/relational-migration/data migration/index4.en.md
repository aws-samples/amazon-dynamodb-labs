---
title : "VIEW migration"
weight : 33
---

## Migrating from a VIEW

In the previous step, you simply ran ```./migrate.sh Customers``` to perform a migration of this table 
and data to DynamoDB.

You can repeat this process to migrate the custom view vCustOrders.

1. Run:
```bash
./migrate.sh vCustOrders
```

The script assumes you want a two-part primary key of Partition Key and Sort Key, found in the two leading columns.

In case you want a Partition Key only table, you could specify this like so.
```bash
./migrate.sh vCustOrders 1
```
However, this is not advisable since this particular dataset is not unique by just the first column.

![View output](/static/images/relational-migration/view_result.png)

::alert[Import will write all the records it finds in the bucket to the table. If a duplicate record is encountered, it will simply overwrite it. Please be sure that your S3 data does not contain any duplicates based on the Key(s) of the new table you define.]{header="Note:"}

The second import is also not advisable since if you created a new vCustOrders table in step 1, the second Import attempt would not be able to replace the existing table, and would fail.
