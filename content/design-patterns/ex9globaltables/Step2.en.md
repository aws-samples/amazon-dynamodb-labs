+++
title = "Step 2 - Load data into the global table and query the replica"
date = 2019-12-02T10:50:03-08:00
weight = 2
+++


Insert a new item to the `recommendations` table in US West (Oregon).

```bash
aws dynamodb put-item \
    --table-name recommendations\
    --item '{"customer_id": {"S":"99"},"category_id": {"S":"Drama"}}' \
    --region us-west-2
```
Wait for a second, and query the replica

```bash
aws dynamodb get-item \
    --table-name recommendations \
    --key '{"customer_id": {"S":"99"},"category_id": {"S":"Drama"}}' \
    --region us-east-1
```
Now, run the script that sequentially writes items to the local region and queries the remote region, measuring the replication time. This is done for 10 items

```bash
python load_recommendations_sequentially.py recommendations ./data/recommendations.csv
```

The sample `recommendations.csv` record looks like the following:
```csv
001,Drama, Argo
```
In addition to the customer_id and category_id, we now have the movie title. The script reads each record from the csv file and puts the item into the DynamoDB table in the Us West (Oregon) region. Immediately, it runs a GetItem for that customer_id from the replica table in the US East (N. Virgina) regionr, which returns an empty record. It waits for a second and tries again. Now the replica returns the item for the newly inserted customer id. The following output shows this pattern for a few items.
Output:
```txt
88e9fe579ead:design-patterns ssarma$ python load_recommendations_sequentially.py recommendations ./data/recommendations.csv
[]
Current time: 1611813327.91749
[{'category_id': 'Drama', 'customer_id': '001', 'title': ' Argo'}]
Current time: 1611813329.044519

[]
Current time: 1611813329.2009711
[{'category_id': 'Thriller', 'customer_id': '002', 'title': 'The Last Seven'}]
Current time: 1611813330.320935

[]
Current time: 1611813330.476702
[{'category_id': 'Comedy', 'customer_id': '003', 'title': "The Night They Raided Minsky's"}]
Current time: 1611813331.594492

[]
Current time: 1611813331.7503822
[{'category_id': 'Thriller', 'customer_id': '004', 'title': 'The Final Destination'}]
Current time: 1611813332.870115
```
The output confirms that 10 items have been inserted to the table. 

You can review the replication metrics for the `recommendations` table in the DynamoDB console (as shown in the following screenshot) by choosing the **recommendations** table and then choosing the **Monitor** tab.

![Recommendations table](/images/awsconsole9b.png)

Scroll down to the Latency section to see the Get, Put and Query latency metrics

![Recommendations table](/images/awsconsole9c.png)

You can use Amazon CloudWatch to monitor the behavior and performance of a global table. Amazon DynamoDB publishes ReplicationLatency metric for each replica in the global table.
ReplicationLatency is the elapsed time between when an item is written to a replica table, and when that item appears in another replica in the global table. ReplicationLatency is expressed in milliseconds and is emitted for every source and destination Region pair. During normal operation, ReplicationLatency should be fairly constant. An elevated value for ReplicationLatency could indicate that updates from one replica are not propagating to other replica tables in a timely manner. Over time, this could result in other replica tables falling behind because they no longer receive updates consistently. In this case, you should verify that the read capacity units (RCUs) and write capacity units (WCUs) are identical for each of the replica tables. In addition, when choosing WCU settings, follow the recommendations in Best Practices and Requirements for Managing Capacity. ReplicationLatency can increase if an AWS Region becomes degraded and you have a replica table in that Region. In this case, you can temporarily redirect your application's read and write activity to a different AWS Region. 
For more information, see DynamoDB Metrics and Dimensions.
