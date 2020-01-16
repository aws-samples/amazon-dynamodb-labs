+++
title = "Step 2 - Scan employees to find managers without using the GSI"
date = 2019-12-02T10:57:23-08:00
weight = 2
+++

To start, you will scan the table to find all the managers without using the GSI. In this case, you need to use a filter expression to return only the items where the attribute is_manager is equal to 1.
```py
fe = "is_manager = :f"
eav = {":f": "1"}
response = table.scan(
  FilterExpression=fe,
  ExpressionAttributeValues=eav,
  Limit=pageSize
)
```
Run the following command:
```bash
python scan_for_managers.py employees 100
```
Parameters: 1. Table name = **employees** 2. Page size = **100**, this is size of the pagination for the scan

You can see the output including the scanned count and the execution time:
```txt
Managers count: 84. # of records scanned: 4000. Execution time: 0.596132993698 seconds
```
**Note**: *Observe the number of items scanned to return the values. If you receive an error, please ensure you completed Step 1 and both indexes appear as ACTIVE*
