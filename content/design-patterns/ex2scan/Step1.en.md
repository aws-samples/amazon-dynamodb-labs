+++
title = "Step 1 - Execute a sequential Scan"
date = 2019-12-02T10:35:42-08:00
weight = 1
+++

First, execute a simple (sequential) `Scan` to calculate the total bytes sent for all records with `response code <> 200`. You can run a `Scan` with a filter expression to filter out unrelated records. The application worker will then sum the values of all the returned records where `response code <> 200`.

The Python file, `scan_logfile_simple.py`, includes the command to run a `Scan` with a filter expression and then calculate the sum of bytes sent.

The following code block scans the table.

```py
  fe = "responsecode <> :f"
  eav = {":f": 200}
  response = table.scan(
      FilterExpression=fe,
      ExpressionAttributeValues=eav,
      Limit=pageSize,
      ProjectionExpression='bytessent')
```
**Note:** You can review the file on your own with `vim ~/workshop/scan_logfile_simple.py`. Type `:q` and hit enter to exit vim.

Notice that there is a `Limit` parameter set in the `Scan` command. A single `Scan` operation will read up to the maximum number of items set (if using the `Limit` parameter) or a maximum of 1 MB of data, and then apply any filtering to the results by using `FilterExpression`. If the total number of scanned items exceeds the maximum set by the limit parameter or the data set size limit of 1 MB, the scan stops and results are returned to the user as a `LastEvaluatedKey` value. This value can be used in a subsequent operation so that you can pick up where you left off.

In the following code, the `LastEvaluatedKey` value in the response is passed to the `Scan` method via the `ExclusiveStartKey` parameter.

```py
  while 'LastEvaluatedKey' in response:
    response = table.scan(
        FilterExpression=fe,
        ExpressionAttributeValues=eav,
        Limit=pageSize,
        ExclusiveStartKey=response['LastEvaluatedKey'],
        ProjectionExpression='bytessent')
    for i in response['Items']:
        totalbytessent += i['bytessent']
```
When the last page is returned, `LastEvaluatedKey` is not part of the response, so you know that the scan is complete.

Now, execute this code. 

```bash
python scan_logfile_simple.py logfile_scan
```

**Parameters:** Tablename: `logfile_scan`

The output will look like the following.

```txt
Scanning 1 million rows of table logfile_scan to get the total of bytes sent
Total bytessent 6054250 in 16.325594425201416 seconds
```

Make a note of the time it took for the scan to complete. With this exercise's dataset, a parallel scan will complete faster than the sequential scan.

