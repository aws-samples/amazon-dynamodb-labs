+++
title = "Step 3 - Scan the employees table to find managers by using the sparse global secondary index"
date = 2019-12-02T10:57:24-08:00
weight = 3
+++

TODO How about if we indicate here why we had them not use the global secondary index before using the sparse global secondary index. What is the purpose? Should they be looking for a specific difference in the two experiences? If so, let’s say that here, so they aren’t having to “do the math” themselves. 
Now, scan the new global secondary index, `GSI_2` on the `employees` table.
```py
response = table.scan(
  Limit=pageSize,
  IndexName='GSI_2'
)
```
Run the following AWS CLI command to execute this scan using the sparse index.
```bash
python scan_for_managers_gsi.py employees 100
```
**Parameters:**
1. Table name = `employees`
2. Page size = `100` (this is size of the pagination for the scan).

The following output includes the scanned count and the execution time.
```txt
Number of managers: 84. # of records scanned: 84. Execution time: 0.287754058838 seconds
```
Observe the scanned count and execution time using the sparse index.
TODO Observe how? We need to be explicit in explaining the difference instead of saying “observe this” and not giving any indication of what they’re looking for. 
