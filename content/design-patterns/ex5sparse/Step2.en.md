+++
title = "Step 2 - Scan the employees table to find managers without using the sparse global secondary index"
date = 2019-12-02T10:57:23-08:00
weight = 2
+++

The sparse index pattern cuts the haystack representing your data down into a smaller pile so that your searches on the index, with either the `Scan` or `Query` API, are more efficient. Instead of combing through all the data in the DynamoDB base table, you can create a sparse index to hold a fraction of your information for easy querying and searching. To learn the definition of a [DynamoDB sparse index please review our best practices documentation](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-indexes-general-sparse-indexes.html).

To start, scan the table to find all the managers without using the global secondary index. The throughput consumed will give us a baseline for comparison later in the exercise. In this case, you need to use a filter expression to return only the items where the attribute is_manager is equal to 1, as shown in the following code example.
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
**Parameters:**
1. Table name = `employees`
1. Page size = `100` (this is size of the pagination for the scan).

The following output includes the scanned count and the execution time.
```txt
Managers count: 84. # of records scanned: 4000. Execution time: 0.596132993698 seconds
```
Review the number of items scanned to return the values. The value of the number of records scanned in the above sample output, 4000, should match the number in your script's output. If you receive an error or inconsistency, ensure you completed Step 1 in this exercise and both indexes are `ACTIVE`. Try changing the page size to a larger number such as 1000. The execution time will decrease because there are fewer round trips to DynamoDB. A `Scan` API call can return up to 1MB of data at a time.
