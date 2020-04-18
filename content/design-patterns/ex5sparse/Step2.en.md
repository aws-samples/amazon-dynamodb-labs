+++
title = "Step 2 - Scan the employees table to find managers without using the sparse global secondary index"
date = 2019-12-02T10:57:23-08:00
weight = 2
+++

To start, scan the table to find all the managers without using the global secondary index. The throughput consumed will give us a baseline for comparison laterin the exercise. In this case, you need to use a filter expression to return only the items where the attribute is_manager is equal to 1, as shown in the following code example.
```py
fe = "is_manager = :f"
eav = {":f": "1"}
response = table.scan(
  FilterExpression=fe,
  ExpressionAttributeValues=eav,
  Limit=pageSize
)
```
Run the following AWS CLI command to find all managers without using the global secondary index.
```bash
python scan_for_managers.py employees 100
```
Parameters: 1. Table name = **employees** 2. Page size = **100** (this is size of the pagination for the scan).

The following output includes the scanned count and the execution time.
```txt
Managers count: 84. # of records scanned: 4000. Execution time: 0.596132993698 seconds
```
Observe the number of items scanned to return the values. If you receive an error, ensure you completed Step 1 in this exercise and both indexes are **ACTIVE.**
