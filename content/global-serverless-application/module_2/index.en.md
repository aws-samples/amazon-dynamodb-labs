---
title : "Module 2: Explore Global Tables"
weight : 30
---

### Application Overview
Congratulations! You now have a serverless application stack running in both Oregon and Ireland.
The stacks you deployed with Chalice each contain the following core components:

* **Amazon API Gateway web service** that responds to HTTP GET calls and forwards them to the Lambda function.
* **AWS Lambda function** that performs read and write requests to the DynamoDB table using Python.
* **AWS IAM role** to grant necessary permissions .

You then used the AWS Command Line Interface to deploy a DynamoDB Global Table called **global-serverless** and fill it with several items.
These items represent bookmark records that can be set to record and retrieve the progress a customer has made 
when watching video content. There are also items representing a catalog of video content available.

![Global Serverless Architecture](/static/images/global-serverless-application/module_2/architecture.png "Global Serverless Architecture")


### DynamoDB Global Table Details

#### Bookmark Design
Our table has a two-part primary key consisting of a Partition Key and a Sort Key, named PK and SK.
Each bookmark record will have the viewer's UserID as the PK value, and a ContentID value in the SK to denote the video they are watching.
A third attribute, called Bookmark, will record the progress.  The application will make periodic updates to this Bookmark attribute as the show is watched.
If the user stops and then returns again later, a Get-Item call can locate the bookmark, read the Bookmark value, and queue up the video player
to the right spot for the customer to continue watching.

#### Replication Performance
When the application stack in Oregon makes calls to DynamoDB, it connects to the DynamoDB table in the same region. 
We can call this local table a regional replica since it participates in Global Tables replication.
Writes to any regional replica will be detected by the DynamoDB service and the new item image will be shipped and applied to all other regional replicas.
The goal of Global Tables is to bring all replicas to an identical state as quickly as possible.
Callers such as our Lambda function in Oregon do not need to be aware of other regions and do not connect to any global endpoint since there isn't one.

Write operations to a replica table are confirmed successful to the caller with the same performance
as a non-Global Table, typically within 10 milliseconds. 

The distance between Oregon and Ireland is 4500 miles (7000 km). 
Information traveling at the speed of light will cross this distance in 24 ms.

![distance Oregon to Ireland](/static/images/global-serverless-application/module_2/distance_gt.png "Distance Oregon to Ireland")

The time it takes for DynamoDB to replicate changes to other regions can vary,
but is typically 1-2 seconds. The **ReplicationLatency** statistic in Cloudwatch 
tracks the time required to replicate items.

### Testing Edge Cases in the Web Application

Let's prove that Global Tables replication is working.

1. Click the plus button ```+``` in the first region and notice that the new bookmark value is displayed.
2. Click Get-Item in the second region and compare the value to the bookmark in the first region. 
If they are the same, that means that Global Tables as applied the new state to all regions.
3. Repeat steps 1 and 2 as quickly as possible. 

![Replication Delay](/static/images/global-serverless-application/module_2/gt_replication_delay.png "Replication Delay")

The goal is to check the bookmark in region two before the replication completes. 
Since replication can occur in about one second, you will have to be quick to detect this. 
If you do, then click Get-Item again and the synchronized value should now be shown.  
Note the app keeps a timer after every update, so you can see how many seconds have elapsed when performing a subsequent read.

#### Generate a Conflict
There is an edge case with Global Tables that happens when writes to the same item occur at the same time in different regions.
If the writes conflict during the 1-2 seconds of in-flight replication, 
then DynamoDB detects this as a Conflict, 
and makes a decision on which one of the writes will win the conflict.
The timestamps of the updates are compared, and the later write becomes the winner. 
The earlier write is thrown out as if it never happened.

1. In region one, click Get-Item and note the current bookmark value. 
2. Next, click the plus button.
3. In region two, immediately click the minus button.
4. Carefully examine the output. Did region two change the value back to the starting value? 
If so, then there was no conflict. The first update replicated completely before the second update began.
If the second update took the bookmark lower than the starting value, that shows there WAS a conflict and that 
the first update was un-done.

![Replication Conflict](/static/images/global-serverless-application/module_2/gt_replication_conflict.png "Replication Conflict")


You can read more about DynamoDB Global Tables in the final chapter of this workshop or in the [Global Tables Documentation](https://aws.amazon.com/dynamodb/global-tables/)
