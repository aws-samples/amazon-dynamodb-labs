+++
title = "Global Tables"
date = 2019-12-02T10:17:33-08:00
weight = 5
chapter = true
pre = "<b>Exercise 9: </b>"
description = "Explore how to create global tables and how the replication works across regions."
+++

A DynamoDB global table is a collection of one or more replica tables, one replica per region, all owned by a single AWS account, that DynamoDB treats as a single unit. Every replica has the same table name, the same primary key schema and stores the same set of data items. When an application writes data to a replica table in one Region, DynamoDB propagates the write to the other replica tables in the other AWS Regions automatically. In a global table, a newly written item is usually propagated to all replica tables within a second. You can add replica tables to the global table so that it can be available in additional Regions.

Use Version 2019.11.21 (Current) of global tables along with on-demand capacity. Using on-demand capacity ensures that you always have sufficient capacity to perform replicated writes to all regions of the global table. The number of replicated write request units will be equal in all Regions of the global table. For example, suppose that you expect 10 writes per second to your replica table in N. Virginia, you should expect to consume 10 replicated write request units in N. Virginia. 

When you use the provisioned capacity mode, you manage your auto scaling policy with UpdateTableReplicaAutoScaling. Minimum and maximum throughput and target utilization are established globally for the table and passed to all replicas of the table. For details about autoscaling and DynamoDB, see Managing Throughput Capacity Automatically with DynamoDB Auto Scaling.

When you are using Version 2019.11.21 (Current) of global tables and you also use the Time to Live feature, DynamoDB replicates TTL deletes to all replica tables. The initial TTL delete does not consume write capacity in the region in which the TTL expiry occurs. However, the replicated TTL delete to the replica table(s) consumes a replicated write capacity unit when using provisioned capacity, or replicated write when using on-demand capacity mode, in each of the replica regions and applicable charges will apply. 

Transactional operations provide atomicity, consistency, isolation, and durability (ACID) guarantees only within the region where the write is made originally. Transactions are not supported across regions in global tables. For example, if you have a global table with replicas in the US West (Oregon) and US East (N. Virginia) regions and perform a TransactWriteItems operation in the US West (Oregon) Region, you may observe partially completed transactions in US East (N. Virginia) Region as changes are replicated. Changes will only be replicated to other regions once they have been committed in the source region. 

If the customer managed CMK used to encrypt a replica is inaccessible DynamoDB will remove this replica from the replication group. The replica will not be deleted and replication will stop from and to this region, 20 hours after detecting the AWS KMS key as inaccessible. If you disable an AWS Region, DynamoDB will remove this replica from the replication group, 20 hours after detecting the AWS Region as inaccessible. The replica will not be deleted and replication will stop from and to this region.
