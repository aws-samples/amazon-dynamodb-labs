+++
title = "Amazon DynamoDB Streams and AWS Lambda"
date = 2019-12-02T10:18:15-08:00
weight = 9
chapter = true
pre = "<b>Exercise 8: </b>"
+++


The combination of DynamoDB Streams with AWS Lambda enables many powerful design patterns. In this exercise, you replicate items from one DynamoDB table to another table by using DynamoDB Streams and Lambda functions.

You will reuse the `logfile` table that you created in Exercise 1. You will enable DynamoDB Streams on the `logfile` table. Whenever a change is made to the `logfile` table, this change appears immediately in a stream. Next, you attach a Lambda function to the stream. The purpose of the Lambda function is to query DynamoDB Streams for updates to the `logfile` table and write the updates to a newly created table named `logfile_replica`. The following diagram shows an overview of this implementation.

TODO : The table names in this diagram (tlog and tlog_replica) do not match the table names in the paragraph that introduces this diagram (logfile and logfile_replica). They should match. 
![DynamoDB stream with Lambda](/images/image6.jpg)
