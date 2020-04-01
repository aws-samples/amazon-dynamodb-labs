+++
title = "Step 2 - Querying the GSI with shards"
date = 2019-12-02T10:45:32-08:00
weight = 2
+++


To get all the log records with a 404 response code, you need to query all the global secondary index partitions by using the sort key. You can do that using parallel threads in your application, and by using the partition key and sort key.
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
Run the following script to retrieve the items from the sharded global secondary index by using only the partition key and response code.
```bash
python query_responsecode.py logfile_scan 404
```
This will query the `logfile_scan` table for items with sort keys that begins_with `404`. `begins_with` is a parameter in [the DynamoDB Query's KeyConditionExpression as described in our documentation](https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_Query.html#DDB-Query-request-KeyConditionExpression). A query is run for each shard on the GSI and the results are counted on the client. The output of the script will look like the following.
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
You also can query the same global secondary index for the same response code and specify a date. This will query the `logfile_scan` table for items with sort keys that begins_with `404#2017-07-21`.
```bash
python query_responsecode.py logfile_scan 404 --date 2017-07-21
```
The output will look like the following.
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


#### Review

In this exercise, we used a sharded global secondary index (GSI) to quickly retrieve sorted results, which used composite keys that are covered later in the lab in [Exercise 6]({{< ref "design-patterns/ex6compos" >}}). Use GSI write sharding when you need a scalable sorted index.  
The sharded GSI example used a set range of keys from 0 to 9 inclusive, but in your own application you can choose any range. In your application, you can add more shards as the number of items indexed increase. In each shard, the data is sorted on disk by the sort key. This allowed us to retrieve server access logs sorted by status code and the data, e.g. `404#2017-07-21`.  
For more information on how to choose the right number of shards, read [Choosing the right number of shards for your large-scale Amazon DynamoDB table](https://aws.amazon.com/blogs/database/choosing-the-right-number-of-shards-for-your-large-scale-amazon-dynamodb-table/) on the AWS Database Blog.
