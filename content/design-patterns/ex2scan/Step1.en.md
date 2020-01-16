+++
title = "Step 1 - Execute a simple Scan"
date = 2019-12-02T10:35:42-08:00
weight = 1
+++

First, let's execute a simple (sequential) scan to calculate the total bytes sent for all records with **response code <> 200**. You can run a scan operation with a filter expression to filter out the uninteresting records. The application will then sum up the values of all the returned records where response code <> 200.

The Python file **scan_logfile_simple.py** has the command to do the scan with filter and calculate the sum of bytes sent.

Take a look at the code block used to scan the table:
```py
  fe = "responsecode <> :f"
  eav = {":f": 200}
  response = table.scan(
      FilterExpression=fe,
      ExpressionAttributeValues=eav,
      Limit=pageSize,
      ProjectionExpression='bytessent')
```
**Note:** *You can review the file on your own with ```vim``` with ```vim ~/workshop/scan_logfile_simple.py```. Type ```:q``` and hit enter to exit vim.*

Notice how there is a Limit parameter set in the scan command. A single Scan operation will read up to the maximum number of items set (if using the Limit parameter) or a maximum of 1 MB of data and then apply any filtering to the results using FilterExpression. If the total number of scanned items exceeds the maximum set by the limit parameter (or) the data set size limit of 1 MB, the scan stops and results are returned to the user as a LastEvaluatedKey value, which can then be used in a subsequent operation, so that you can pick up where you left off.

See the code below. The LastEvaluatedKey value in the response is then passed to the subsequent scan method via the ExclusiveStartKey parameter.
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
When the last page is returned, LastEvaluatedKey is not part of the response, so you will know that the scan is complete.

Now lets execute this code we just discussed:
```bash
python scan_logfile_simple.py logfile_scan
```
Parameters: Tablename: **logfile_scan**

Output:
```txt
Scanning 1 million rows of table logfile_scan to get the total of bytes sent
Total bytessent 6054250 in 24.5398740768 seconds
```
Note down the time it took for the scan to complete.
