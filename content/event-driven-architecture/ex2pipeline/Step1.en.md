---
title: "Step 1: Connect StateLambda"
date: 2019-12-02T10:35:42-08:00
weight: 1
---

The objective of this step is to connect the `StateLambda` function with the `IncomingDataStream` Kinesis stream as shown in the diagram below.
When new messages become available in the Kinesis stream, the `StateLambda` function will be invoked to process the stream records. Each stream record contains a single trade.

<!-- TODO explain what's in a stream record -->
![Architecture-1](/images/event-driven-architecture/architecture/step1.png)

## Connect the StateLambda function with a Kinesis Data Stream

1. Use the AWS Management Console and navigate to the AWS Lambda service within the console.
2. Click on the `StateLambda` function to edit its configuration. See the figure below.
3. The function overview shows that the `StateLambda` function doesn't have any triggers yet. Click on the `Add trigger` button.

![Architecture-1](/images/event-driven-architecture/lab1/add-trigger-state-lambda.png)

4. Specify the following configuration (see the figure below for details):
    - In the first drop down select `Kinesis` as the data source.
    - For the Kinesis stream, select `IncomingDataStream`.
    - Set the `Batch size` to `100`.

![Architecture-1](/images/event-driven-architecture/lab1/connect-state-lambda.png)

5. Click `Add` in the bottom right corner to create and enable an event source mapping on the Lambda function.

At this point you have configured an event based connection between Kinesis Data Streams and AWS Lambda. The `StateLambda` function will be invoked whenever new messages appear in the `IncomingDataStream`. The messages will be passed to the Lambda function in batches of up to 100 at a time.

## How do you know it is working?

If everything was done correctly then the `StateLambda` function will be invoked with stream records from the Kinesis stream. Therefore, in one to two minutes you should be able to see logs from the Lambda invocations under the `Monitor` in the `Logs` tab.

![Architecture-1](/images/event-driven-architecture/lab1/state-lambda-logs.png)

You can also observe the outputs of `StateLambda` to verify the connection by reviewing the `Items` section of the DynamoDB console. To do that, navigate to the DynamoDB service in the AWS console, click `Items` on the left, and select `StateTable`.

At this stage you should see multiple rows similar to the image below. The number of items returned may vary. You can click on the orange `Run` button if you want to refresh the items.

![Architecture-1](/images/event-driven-architecture/lab1/state-table-data.png)

Continue on to: [Step 2]({{< ref "event-driven-architecture/ex2pipeline/step2" >}}).
