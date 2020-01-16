+++
title = "Step 5 - Map the DynamoDB Streams with the Lambda function"
date = 2019-12-02T12:34:07-08:00
weight = 5
+++


So far, you have the source table with DynamoDB Streams enabled and the Lambda function, now you need to map the source stream with the Lambda function.

You need to copy the ARN from the previous step to the command below and replace YOUR_STREAM_ARN_HERE and run this:
```bash
aws lambda create-event-source-mapping \
--function-name ddbreplica_lambda --enabled --batch-size 100 --starting-position TRIM_HORIZON \
--event-source-arn YOUR_STREAM_ARN_HERE
```
**Note**: *You must copy the full stream label ARN, including the timestamp on the end*

The expected result is:
```json
{
    "MaximumBatchingWindowInSeconds": 0,
    "UUID": "be5884e0-bcd9-4301-b535-329e8c13bb73",
    "StateTransitionReason": "User action",
    "LastModified": 1607986748.972,
    "BatchSize": 100,
    "DestinationConfig": {
        "OnFailure": {}
    },
    "EventSourceArn": "arn:aws:dynamodb:<REGION>:<ACCOUNTID>:table/logfile/stream/2020-12-31T00:00:00.000",
    "FunctionArn": "arn:aws:lambda:<REGION>:<ACCOUNTID>:function:ddbreplica_lambda",
    "State": "Creating",
    "ParallelizationFactor": 1,
    "LastProcessingResult": "No records processed",
    "MaximumRetryAttempts": 10000,
    "MaximumRecordAgeInSeconds": 604800,
    "BisectBatchOnFunctionError": false
}
```
