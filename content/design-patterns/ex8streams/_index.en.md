+++
title = "Amazon DynamoDB Streams and AWS Lambda"
date = 2019-12-02T10:18:15-08:00
weight = 9
chapter = true
pre = "<b>Exercise 8: </b>"
description = "Learn how to process DynamoDB items with AWS Lambda for endless triggers."
+++


The combination of DynamoDB Streams ([documentation explaining the service](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Streams.html)) with AWS Lambda enables many powerful design patterns. In this exercise, you replicate items from one DynamoDB table to another table by using DynamoDB Streams and Lambda functions.

DynamoDB Streams captures a time-ordered sequence of item-level modifications in any DynamoDB table and stores this information in a log for up to 24 hours. Applications can access this log and view the data items as they appeared before and after they were modified, in near-real time. DynamoDB Streams provides for the following use cases:

- A global multi-player game has a multi-leader database topology, storing data in multiple AWS Regions. Each region stays in sync by consuming and replaying the changes that occur in the remote Regions. (In fact, DynamoDB Global Tables relies on DynamoDB Streams for global replication.)
- A new customer adds data to a DynamoDB table. This event invokes an AWS Lambda function to copy the data to a separate DynamoDB table for long term retention (This is very similar to this exercise, where we copy data from one DynamoDB table to another using DynamoDB Streams.)

You will reuse the `logfile` table that you created in Exercise 1. You will enable DynamoDB Streams on the `logfile` table. Whenever a change is made to the `logfile` table, this change appears immediately in a stream. Next, you attach a Lambda function to the stream. The purpose of the Lambda function is to query DynamoDB Streams for updates to the `logfile` table and write the updates to a newly created table named `logfile_replica`. The following diagram shows an overview of this implementation.

![DynamoDB stream with Lambda](/images/image6.jpg)
