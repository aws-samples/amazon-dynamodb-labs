---
title: "Build a Serverless Event Driven Architecture with DynamoDB"
chapter: true
description: "400 level: Hands-on exercise using Python and DynamoDB Streams."
pre: "<b>LEDA: </b>"
weight: 1
---
In this workshop you will be presented with a serverless event-driven data aggregation pipeline. It's built with [AWS Lambda](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html), [Amazon DynamoDB](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html), and [Amazon Kinesis Data Streams](https://docs.aws.amazon.com/streams/latest/dev/introduction.html).

While you may be happy to partake in this workshop, be aware that the pipeline is broken and it needs your attention to get running! As you will soon discover, the workshop is designed with an input stream that contains duplicates and Lambda functions that randomly fail.

Over the course of two labs you will have to first connect all the elements of the pipeline, and then update the Lambda functions to avoid message loss or duplication under (induced) random failures.

Here's what this workshop includes:

{{% children  depth="1" description="true" %}}

### Target audience

The workshop is intended for anyone interested in understanding how to build serverless data processing pipelines. Basic understanding of AWS services and experience in Python programming is desirable but not required. We classify this as a 300-level workshop, which means you don't need to be an expert on any of the three services that are the focus.

### Requirements
#### Basic knowledge of AWS services
- Among other services this lab will guide you through the use of Amazon Kinesis Data Streams and AWS Lambda

#### Basic understanding of DynamoDB
- If you're not familiar with DynamoDB or are not participating in this lab as part of an AWS event, consider reviewing the documentation on "[What is Amazon DynamoDB?](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html)"

#### Familiarity with Python/Boto3
- You will be copying as pasting code so you can focus on learning about DynamoDB.
- You will be able to review all code run during the exercises.

#### Duration

The workshop requires approximately 2 hours to complete.

### Outcomes

- Using practical examples, understand how to connect serverless AWS components into an event driven pipeline.
- Understand how to leverage special features of DynamoDB and Lambda to build a reliable data processing pipeline with exactly once processing semantics.
- Understand various error modes and retry mechanisms.
