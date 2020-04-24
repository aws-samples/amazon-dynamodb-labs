+++
title = "Step 4 - Enable DynamoDB Streams"
date = 2019-12-02T12:34:07-08:00
weight = 4
+++

Now that we have an AWS Lambda function created to process the DynamoDB Streams records, we need to enable the DynamoDB Stream on the `logfile` table. In the following step we will connect the stream with the function.


Enable DynamoDB Streams for the `logfile` table.
```bash
aws dynamodb update-table --table-name 'logfile' --stream-specification StreamEnabled=true,StreamViewType=NEW_IMAGE
```
Get the full ARN for DynamoDB Streams in the response.
```bash
aws dynamodb describe-table --table-name 'logfile' --query 'Table.LatestStreamArn' --output text
```
The output will look like the following
```
arn:aws:dynamodb:<REGION>:<ACCOUNTID>:table/logfile/stream/2018-10-27T02:15:46.245
```
You need the ARN for the next step.
