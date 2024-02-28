---
title: "3. Change Data Capture using DynamoDB Streams"
date: 2023-12-01T00:00:00-00:00
weight: 10
chapter: true
---

[DynamoDB streams](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Streams.html) records a time ordered sequence of item level changes that occur on a DynamoDB table. Once enabled, information about all item level changes will be logged and stored for up to 24 hours.

Changes to items on DynamoDB tables with streams enabled are captured in near real-time so the events can be used as triggers for event driven applications that consume data from your DynamoDB stream.

In this chapter, you enable DynamoDB streams on the Orders table and deploy an AWS Lambda function that copies changes from the Orders table to the OrdersHistory table every time an item is updated on the Orders table.

The resulting solution is shown in the image below.

![Final Deployment Architecture](/static/images/change-data-capture/cdc-ddbs/create-order-history-ddbs.png)
