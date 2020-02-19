+++
title = "Global Secondary Index Write Sharding"
date = 2019-12-02T10:17:22-08:00
weight = 4
chapter = true
pre = "<b>Exercise 3: </b>"
+++


The primary key of a DynamoDB table (or the global secondary index) consists of a partition key and a sort key (optional). The way you design the content of those keys is extremely important for the structure and performance of your database. Partition-key values determine the logical partitions in which the data is stored. Therefore it is important to choose a partition key value that uniformly distributes the workload across all partitions in the table (or the GSI).

In this exercise, we will discuss GSI write-sharding which is an effective design pattern to selectively query the items spread across different logical partitions in a very large table. Let's review the Server Logs example. This time, we will query the items with response code 4xx. Note that the items with response code 4xx are a very small percentage of the total data and do not have an even distribution by response code. For example, the code "200 OK" has much more records than the others as expected for any application. You can see the distribution of the log records by response code for the sample file **logfile_medium1.csv** in the graph below.

**Figure - Log records by response code**
![Log records by response code](/images/image8.jpg)

We will create a write-sharded GSI on the table to randomize the writes across multiple logical partition key values. In effect, we will increase the write and read throughput of the application. To apply this design pattern, you can create a random number from a fixed set (for example, 1 to 10) and use this number as the logical partition key for a GSI. Because you are randomizing the partition key, the writes to the table are spread evenly across all of the partition key values independent of any attribute; this will yield better parallelism and higher overall throughput. Also, if the application needs to query the log records by a specific response code in a specific date, you can create a composite sort key using a combination of the response code and the date.

In this exercise, we will create a GSI using the random values for the Partition Key and the composite key "responsecode#date#hourofday" as the Sort Key. The table **logfile_scan** that was created and populated during the preparation phase of the workshop already has these two attributes. The attributes were created using the following code:
```py
SHARDS = 10
newitem['GSI_1_PK'] = "shard#{}".format((newitem['requestid'] % SHARDS) + 1)
newitem['GSI_1_SK'] = row[7] + "#" + row[2] + "#" + row[3]
```
