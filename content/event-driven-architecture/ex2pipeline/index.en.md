---
title: "Connect the pipeline"
date: 2019-12-02T10:17:10-08:00
weight: 3
chapter: true
pre: "<b>Lab 1: </b>"
description: "Process streaming data to create an end-to-end data processing pipeline"
---

### Let’s go deep on streaming data sources with AWS Lambda!


In this first lab you will process streaming data to create an end-to-end data processing pipeline. You will use Amazon Kinesis, AWS Lambda, Amazon DynamoDB and one of its powerful features called DynamoDB Streams to accomplish this. We will take some time to explain some of the key features of these services.

### Amazon DynamoDB

Amazon DynamoDB is a massive horizontally scaled NoSQL database designed for single-digit-millisecond latency with virtually no limits in scale, either in throughput or in storage. DynamoDB offers built-in security, continuous backups, automated multi-region replication, in-memory caching, and data export tools.

This diagram shows the features and integrations for DynamoDB:

![DynamoDB ecosystem](/static/images/event-driven-architecture/lab1/dynamodb-ecosystem.png)
If you want to learn more [you can review the DynamoDB's features page on aws.amazon.com](https://aws.amazon.com/dynamodb/features/)


### DynamoDB Streams

DynamoDB Streams provides an ordered set of changes from your DynamoDB table for up to 24 hours after items are written. It is a change data capture (CDC) service, and once you enable the stream on your table changes begin to flow into the stream. DynamoDB item mutations appear exactly once in the stream, and the mutation usually includes the old and new copy of the item but you can choose to have one or the other, or to only have the item keys. The service is durable and highly available. While similar in name to Kinesis Data Streams, DynamoDB Streams has a completely different roadmap, engineering team, and server fleet.

A DynamoDB `stream` is made of many shards. A `shard` contains a time-ordered list of changes from one `DynamoDB partition`. The item changes are put into the shard as `stream records`. Let's unpack these terms:
- `Stream`: A single stream of DynamoDB Streams, which contains CDC data from exactly one DynamoDB table. Streams can be enable or disabled, and at the time of enablement you can choose whether old and new item copies are kept, only one or the other are kept, or only keys. Every stream has a unique id called a *stream label*.
- `DynamoDB partition`:  A partition is an allocation of storage for a table, backed by solid state drives (SSDs) and automatically replicated across multiple Availability Zones within an AWS Region. Every DynamoDB item will reside on exactly one partition, but the partition is 3-way replicated for durability and availability. Changes from a DynamoDB partition are copied into a stream shard in less than a second.
- `Shard`: A stream shard holds stream records. A stream is made up of many stream shards. In DynamoDB, a partition will write to exactly one stream shard, and the two are not to be confused. A stream shard is either open (new stream records can be added) or closed (no stream records can be added). A closed stream shard is defined as a shard with an *EndingSequenceNumber*, whereas an open stream shard as no *EndingSequenceNumber*. To learn more about shards and shard lineage, see our documentation on [Reading and Processing a Stream](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Streams.html#Streams.Processing).
- `Stream record`: A single mutation on the DynamoDB table. Any create, update, or delete operation on the table can generate a stream record so long as the item was actually modified. If you delete an item that doesn't exist or "update" an item but there is no change to its attributes, a stream record is not created. A record has an ApproximateCreationDateTime timestamp accurate to the nearest millisecond for ordering across all shards along with a sequence number that can be used for ordering inside the shard, only. Stream records and the content types (NEW_IMAGE | OLD_IMAGE | NEW_AND_OLD_IMAGES | KEYS_ONLY) [are explained in our StreamRecord documentation](https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_streams_StreamRecord.html).

#### DynamoDB Streams shard lineage

When 4 hours has elapsed, when a shard reaches a predetermined size in bytes, or when a DynamoDB partition splits a shard is closed and new one(s) are created. With the exception of the first shards made when a stream is enabled, all shards have a parent shard. In order for a client such as Lambda to retrieve stream records, they must determine the shard lineage by retrieving all information about shards using the parent shard id to find which shards are the oldest and which are the newest.

Consider a DynamoDB table with 4 partitions. Shards are changed over every 4 hours, for each partition. As you may know, there's a 1:1 mapping between an open shard and a DynamoDB partition. Once the stream has been enabled for 24 hours (the longest retention time for stream data), there will be [(4 partitions) * (24 hours / 4 hours per shard)] = 24 stream shards. At any one time only four will be open and the rest will be closed. When you connect a Lambda function to this stream, there will be four Lambda instances.

Let's take some time to explain this connection and define what a Lambda instance is.

### AWS Lambda Triggers

AWS Lambda is a serverless, event-driven compute service that lets you run code for virtually any type of application or backend service without provisioning or managing servers. Lambda supports many triggers including Kinesis Data Streams and DynamoDB. In this lab you will connect several functions to streaming sources, setting the batch size and concurrency. For this reason we will take time to explain how they work.


The Lambda service supports `Lambda function` triggers through what is called a `event source mapping`. When a Lambda function is connected to a streaming source, you choose whether to begin with the oldest records in the stream or the newest by setting the `StartingPosition` in the event source mapping. Then the Lambda service begins to poll the stream. The Lambda polling service then hands batches of records (size defined by the `BatchSize` in the event source mapping) to a `Lambda instance`. You can limit the number of concurrent Lambda instances using `reserved concurrency`.

- `Lambda function`: From the documentation: *A function is a resource that you can invoke to run your code in Lambda. A function has code to process the events that you pass into the function or that other AWS services send to the function.* In this lab, we have three Lambda functions under your control.
- `Reserved concurrency`: Reserved concurrency guarantees the maximum number of concurrent instances for the function. You can reserve concurrency to prevent your function from using all the available concurrency in the account, or from overloading downstream resources. In this lab we modify one function's concurrency to 1.
- `Lambda instance`: A single instance (a running container) of a Lambda function. Through reserved concurrency with streaming sources, the number of concurrently running Lambda instances can be controlled, however you have no control over the total number of instances. With streaming sources like DynamoDB, Lambda creates one instance for every interesting stream shard by default.
- `Event source mapping`: Event source mappings are the logical connection between a data source and a Lambda function. When you add a trigger to your Lambda function in the lab, the console calls [*CreateEventSourceMapping*](https://docs.aws.amazon.com/lambda/latest/dg/API_CreateEventSourceMapping.html) to link the streaming source to the Lambda function. The API documentation provides many options, but we'll point out three interesting ones:
    - `BatchSize`: The maximum number of stream records Lambda provides your Lambda function instance when its invoked. The Lambda function will need to process those records and return them in a timely manner. A batch size of 1 would be very inefficient because of the overhead of function invocation. The maximum value is 1,000 for DynamoDB Streams.
    - `StartingPosition`: The position in a stream from which to start reading. With *TRIM_HORIZON*, Lambda will begin reading from the oldest data in the stream. With *LATEST*, Lambda will begin reading from the newest shards (the open stream shards, as defined above). As mentioned before, there is one Lambda instance per interesting shard. Over time, there can be more shards added to a stream in which case the number of running instances will grow to match the number of interesting shards. Lambda will discover the shard lineage so it can decide which shards are interesting to begin (the oldest ones, or the newest ones depending on this parameter setting). In this lab we will use the setting *LATEST*.
    - *ParallelizationFactor*: How many Lambda instances to create per stream shard. The default is 1, but you could increase it to 10 instances per shard. With a value above 1, the Lambda service uses a consistent hashing scheme to make sure the same DynamoDB item keys are passed to the same instance, maintaining the ordering of the stream shard. ParallelizationFactor essentially "shards" a stream shard to increase processing speed when your Lambda function code is inefficient or the code's task is complex or slow to complete. We don't set this value during the lab.


Now that you've learned way more about Lambda and DynamoDB than you thought possible (or perhaps more conservatively, you've skim-read more text than you expected to see on this page), let's begin Lab 1 in earnest!

Continue on to: [Step 1]({{< ref "event-driven-architecture/ex2pipeline/step1" >}})
