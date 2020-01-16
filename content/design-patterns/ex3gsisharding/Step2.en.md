+++
title = "Step 2 - Querying the GSI with shards"
date = 2019-12-02T10:45:32-08:00
weight = 2
+++


To get all the log records with response code equals to 404, you need to query all the GSI partitions using the sort key. You can do that using parallel threads in your application, and using the hash key and sort key.
```py
  if date == "all":
    ke = Key('GSI_1_PK').eq("shard#{}".format(shardid)) & Key('GSI_1_SK').begins_with(responsecode)
  else:
    ke = Key('GSI_1_PK').eq("shard#{}".format(shardid)) & Key('GSI_1_SK').begins_with(responsecode+"#"+date)

  response = table.query(
    IndexName='GSI_1',
    KeyConditionExpression=ke
    )
```
Run the script to retrieve the items from the sharded GSI using only the partition key, response code:
```bash
python query_responsecode.py logfile_scan 404
```
The output will look like this:
```txt
Records with response code 404 in the shardid 0 = 0
Records with response code 404 in the shardid 1 = 1750
Records with response code 404 in the shardid 2 = 2500
Records with response code 404 in the shardid 3 = 1250
Records with response code 404 in the shardid 4 = 1000
Records with response code 404 in the shardid 5 = 1000
Records with response code 404 in the shardid 6 = 1750
Records with response code 404 in the shardid 7 = 1500
Records with response code 404 in the shardid 8 = 3250
Records with response code 404 in the shardid 9 = 2750
Number of records with responsecode 404 is 16750. Query time: 1.5092344284057617 seconds
```
If you query the same GSI for the same response code but specifying a date.
```bash
python query_responsecode.py logfile_scan 404 --date 2017-07-21
```
The output will look like this:
```txt
Records with response code 404 in the shardid 0 = 0
Records with response code 404 in the shardid 1 = 750
Records with response code 404 in the shardid 2 = 750
Records with response code 404 in the shardid 3 = 250
Records with response code 404 in the shardid 4 = 500
Records with response code 404 in the shardid 5 = 0
Records with response code 404 in the shardid 6 = 250
Records with response code 404 in the shardid 7 = 1000
Records with response code 404 in the shardid 8 = 1000
Records with response code 404 in the shardid 9 = 1000
Number of records with responsecode 404 is 5500. Query time: 1.190359354019165 seconds
```

You have completed exercise #3!
