+++
title = "Step 3 - Scan the employees table to find managers by using the sparse global secondary index"
date = 2019-12-02T10:57:24-08:00
weight = 3
+++

<<<<<<< HEAD

Now, scan the new global secondary index, *GSI_2* on the *employees* table.  In using our new, sparse index, we expect that we'll consume read capacity for fewer items.  We'll use the sparse index as a very effective filter to improve efficiency for this access pattern.
=======
TODO How about if we indicate here why we had them not use the global secondary index before using the sparse global secondary index. What is the purpose? Should they be looking for a specific difference in the two experiences? If so, let’s say that here, so they aren’t having to “do the math” themselves. 
Now, scan the new global secondary index, `GSI_2` on the `employees` table.
>>>>>>> cf05ae3a723921891ee53bcef8c18313b7bf85c3
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
<<<<<<< HEAD
Observe the scanned count and execution time using the sparse index.  How does this compare to the result achieved from the Scan of the base table (primary index) in Step 2 ?
=======
Observe the scanned count and execution time using the sparse index.
TODO Observe how? We need to be explicit in explaining the difference instead of saying “observe this” and not giving any indication of what they’re looking for. 
>>>>>>> cf05ae3a723921891ee53bcef8c18313b7bf85c3
