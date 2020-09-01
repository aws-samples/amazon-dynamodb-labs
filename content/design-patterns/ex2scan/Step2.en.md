+++
title = "Step 2 - Execute a parallel Scan"
date = 2019-12-02T10:35:42-08:00
weight = 2
+++


To perform a parallel `Scan`, each application worker issues its own `Scan` request with the following parameters:

- `Segment`: The segment to be scanned by a specific application worker. Each worker should use a different value for `Segment`.
- `TotalSegments`: The total number of segments for the parallel scan. This value must be the same as the number of workers that your application will use.

Review the following code block for the parallel scan, which is from the file `scan_logfile_parallel.py`.


```py
  fe = "responsecode <> :f"
  eav = {":f": 200}
  response = table.scan(
    FilterExpression=fe,
    ExpressionAttributeValues=eav,
    Limit=pageSize,
    TotalSegments=totalsegments,
    Segment=threadsegment,
    ProjectionExpression='bytessent'
    )
```

After the first scan, you can continue scanning the table until `LastEvaluatedKey` equals null.

```py
  while 'LastEvaluatedKey' in response:
    response = table.scan(
        FilterExpression=fe,
        ExpressionAttributeValues=eav,
        Limit=pageSize,
        TotalSegments=totalsegments,
        Segment=threadsegment,
        ExclusiveStartKey=response['LastEvaluatedKey'],
        ProjectionExpression='bytessent')
    for i in response['Items']:
        totalbytessent += i['bytessent']
```
To run this code, execute the following AWS CLI command.
```bash
python scan_logfile_parallel.py logfile_scan 2
```
**Parameters:**
1. Table name: `logfile_scan`
1. Number of threads: `2` (this is number of threads to be executed in parallel, which will be used for the number of segments as well).

The output will look like the following.

```txt
Scanning 1 million rows of the `logfile_scan` table to get the total of bytes sent

Total bytessent 6054250 in 8.544446229934692 seconds
```

**Note:** The execution time using a parallel scan will be shorter than the execution time for a sequential scan. The difference in execution time will be even more exaggerated for larger tables.

#### Summary
In this exercise, we have demonstrated use of two methods of DynamoDB table scanning: sequential and parallel, to read items from a table or secondary index. Use `Scan` sparingly because it can consume large amounts of capacity resources. Sometimes a `Scan` is appropriate (such as scanning a small table) or unavoidable (such as performing a bulk export of data). However, as a general rule, you should design your applications to avoid performing scans.

