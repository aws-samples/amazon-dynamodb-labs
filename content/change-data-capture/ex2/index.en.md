---
title: "4. Change Data Capture using Kinesis Data Streams"
date: 2023-12-01T00:00:00-00:00
weight: 15
chapter: true
---

[Amazon Kinesis Data Streams](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/kds.html) can be used to collect and process large streams of data records from applications that produce streaming data in real-time. At a high level, data producers push data records to Amazon Kinesis Data Streams and consumers can read and process the data in real-time.

Data on Amazon Kinesis Data Streams is by default available for 24 hours after the data is written to the stream and the retention period can be increased to a maximum of 365 days.

Amazon DynamoDB has naitve integration with Kinesis streams so Kinesis Data Streams can also be used to record item level changes to DynamoDB tables.

In this chapter, you will repeat the process of capturing item level changes on a DynamoDB table and write those changes to a different DynamoDB table. But in this section, change data capture will be done using Amazon Kinesis Data Streams.

The architecture of the resulting solution is shown in the image below.

![Final Deployment Architecture](/static/images/change-data-capture/cdc-kds/create-order-history-kds.png)
