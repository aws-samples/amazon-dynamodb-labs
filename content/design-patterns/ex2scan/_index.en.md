+++
title = "Table Scan and Parallel Table Scan"
date = 2019-12-02T10:17:10-08:00
weight = 3
chapter = true
pre = "<b>Exercise 2: </b>"
+++


This exercise will demonstrate the two methods of table scan, sequential and parallel.

Even though DynamoDB distributes a large table data across multiple physical partitions, a Scan operation can only read one partition at a time. For this reason, the throughput of a Scan is constrained by the maximum throughput of a single partition.

In order to maximize the utilization of the table level provisioning, use the Parallel Scan operation to logically divide a table (or secondary index) into multiple segments, and use multiple application workers to scan these logical segments in parallel.

**Figure - [Parallel Scan](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Scan.html#Scan.ParallelScan)**

![Parallel Scan](/images/image7.jpg)
