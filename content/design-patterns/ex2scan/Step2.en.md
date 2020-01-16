+++
title = "Step 2 - Execute a parallel scan"
date = 2019-12-02T10:35:42-08:00
weight = 2
+++


To perform a parallel scan, each worker issues its own Scan request with the following parameters:

**Segment**: A segment to be scanned by a particular worker. Each worker should use a different value for Segment.

**TotalSegments**: The total number of segments for the parallel scan. This value must be the same as the number of workers that your application will use.

Take a look at the code block from the **scan_logfile_parallel.py** for the parallel scan.

We need to include the parameters:
- **Segment**: For a parallel Scan request, Segment identifies an individual segment to be scanned by an application worker.
- **TotalSegments**: For a parallel Scan request, TotalSegments represents the total number of segments into which the Scan operation will be divided. The value of TotalSegments corresponds to the number of application workers that will perform the parallel scan.

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

And after the first scan, we can continue scanning the table until LastEvaluatedKey equals null.
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
To run the code execute the following command:
```bash
python scan_logfile_parallel.py logfile_scan 2
```
Parameters: 1) Table name: **logfile_scan** 2) Number of threads: **2** , this is number of threads to be executed in parallel, it will be used for number of segments as well.

Output:
```txt
Scanning 1 million rows of table logfile_scan to get the total of bytes sent
Total bytessent 6054250 in 13.4376678467 seconds
```
**Note**: *The execution time using parallel scan will be shorter than the execution time for a regular scan. The difference will be even larger for larger tables*.
