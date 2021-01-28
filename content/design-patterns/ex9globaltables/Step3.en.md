+++
title = "Step 3 - Write to both regions and see the occasional conflict resolution"
date = 2019-12-02T10:50:04-08:00
weight = 3
+++

You can run the following parallel command to write to both regions at the same time. The region field updates the region that won in the conflict resolution process for each of the 10 items.

```py
parallel --jobs 2 < tasks.txt
```

The script should give you output that looks like the following.
```txt
88e9fe579ead:design-patterns ssarma$ parallel --jobs 2 < tasks.txt
[{'category_id': 'Drama', 'customer_id': '001', 'region': 'West', 'title': ' Argo'}]
Current time: 1611816863.0019908
[{'category_id': 'Drama', 'customer_id': '001', 'region': 'East', 'title': ' Argo'}]
Current time: 1611816864.047831

[{'category_id': 'Thriller', 'customer_id': '002', 'region': 'West', 'title': 'The Last Seven'}]
Current time: 1611816864.1282911
[{'category_id': 'Thriller', 'customer_id': '002', 'region': 'East', 'title': 'The Last Seven'}]
Current time: 1611816865.172729

[{'category_id': 'Comedy', 'customer_id': '003', 'region': 'West', 'title': "The Night They Raided Minsky's"}]
Current time: 1611816865.252855
[{'category_id': 'Comedy', 'customer_id': '003', 'region': 'West', 'title': "The Night They Raided Minsky's"}]
Current time: 1611816866.297246

[{'category_id': 'Thriller', 'customer_id': '004', 'region': 'West', 'title': 'The Final Destination'}]
Current time: 1611816866.377374
[{'category_id': 'Thriller', 'customer_id': '004', 'region': 'West', 'title': 'The Final Destination'}]
Current time: 1611816867.41737
```
You can review the transaction conflict errors  metrics for the `recommendations` table in the DynamoDB console (as shown in the following screenshot) by choosing the **recommendations** table and then choosing the **Monitor** tab.

![Recommendations table](/images/awsconsole9b.png)

Scroll down to the  Transactions section to see the Transaction conflict errors. The chart should say No data available. This is because DynamoDB does the conflict resolution automatically.
![Recommendations table](/images/awsconsole9d.png)

#### Summary

Congratulations, you have completed this exercise and demonstrated how global tables do cross region replications and resolve conflicts. Use DyanmoDB global tables to run your applications that read and write from multiple AWS regions. In the next exercise, you will learn how transactions work in DynamoDB.
