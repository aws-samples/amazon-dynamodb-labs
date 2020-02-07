+++
title = "Amazon DynamoDB Streams and AWS Lambda"
date = 2019-12-02T10:18:15-08:00
weight = 9
chapter = true
pre = "<b>Exercise 8: </b>"
+++


The combination of DynamoDB Streams with AWS Lambda enables many powerful design patterns. In this exercise we will demonstrate a simple way to replicate items from one DynamoDB table to another table using DynamoDB Streams and Lambda functions.

We will re-use the table "logfile" that was created in the earlier exercise. We will enable Streams on "logfile" table. Whenever there is a change in the "logfile" table this change will appear on the Streams immediately. Next, we will attach a Lambda function to the Streams. The purpose of the Lambda function will be to query the Streams for updates to the "logfile" table and write them to a newly created table named "logfile_replica". The figure below shows the high-level view of this implementation.

**Figure - DynamoDB stream with Lambda**
![DynamoDB stream with Lambda](/images/image6.jpg)
