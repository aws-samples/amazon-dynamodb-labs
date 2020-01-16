+++
title = "Step 3 - Scan employees to find managers using the sparse index"
date = 2019-12-02T10:57:24-08:00
weight = 3
+++


Now, you will scan the new GSI *GSI_2* on the employees table.
```py
response = table.scan(
  Limit=pageSize,
  IndexName='GSI_2'
)
```
Run the following command to execute the scan using the sparse index.
```bash
python scan_for_managers_gsi.py employees 100
```
Parameters: 1) Table name = **employees** 2) Page size = **100**, this is size of the pagination for the scan

You can see the output including the scanned count and the execution time:
```txt
Number of managers: 84. # of records scanned: 84. Execution time: 0.287754058838 seconds
```
**Note**: *Observe the scanned count and execution time using the sparse index.*
