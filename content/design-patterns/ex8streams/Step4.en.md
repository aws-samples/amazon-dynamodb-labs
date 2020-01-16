+++
title = "Step 4 - Enable DynamoDB Streams"
date = 2019-12-02T12:34:07-08:00
weight = 4
+++


Enable DynamoDB Streams for the table logfile:
```bash
aws dynamodb update-table --table-name 'logfile' --stream-specification StreamEnabled=true,StreamViewType=NEW_IMAGE
```
Get the full ARN for the DynamoDB Streams in the response, as shown below.
```bash
aws dynamodb describe-table --table-name 'logfile' --query 'Table.LatestStreamArn' --output text
```
The output will be like:
```
arn:aws:dynamodb:<REGION>:<ACCOUNTID>:table/logfile/stream/2018-10-27T02:15:46.245
```
**You will need the ARN for the next command.**
