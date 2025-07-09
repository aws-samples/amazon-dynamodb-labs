---
title: "Enable Kinesis Data Streams"
date: 2023-12-01T00:00:00-00:00
weight: 205
chapter: true
---

Disable DynamoDB streams for the Orders table using the AWS CLI commands below.

```bash
aws dynamodb update-table \
    --table-name Orders \
    --stream-specification \
        StreamEnabled=false \
    --query "Table.StreamSpecification.StreamEnabled"
```

Confirm that DynamoDB streams has been disabled using the AWS CLI commands below.

```bash
aws dynamodb describe-table \
    --table-name Orders \
    --query "Table.StreamSpecification.StreamEnabled"
```

The output should return a boolean as shown below.

```
null
```

Create a Kinesis data stream named **Orders** using the following command.
```bash
aws kinesis create-stream --stream-name Orders --shard-count 2
```
Confirm that the stream is active using the following command.

```bash
aws kinesis describe-stream \
    --stream-name Orders \
    --query "StreamDescription.[StreamStatus, StreamARN]"
```

Sample output:

```
[
    "ACTIVE",
    "arn:aws:kinesis:${REGION}:${ACCOUNT_ID}:stream/Orders"
]
```

Enable Kinesis streaming for the Orders DynamoDB table using following command. Copy the ARN from the previous command into the *--stream-arn* parameter.

```bash
aws dynamodb enable-kinesis-streaming-destination \
    --table-name Orders \
    --stream-arn arn:aws:kinesis:${REGION}:${ACCOUNT_ID}:stream/Orders
```

Sample output:

```
{
    "TableName": "Orders",
    "StreamArn": "arn:aws:kinesis:${REGION}:${ACCOUNT_ID}:stream/Orders",
    "DestinationStatus": "ENABLING",
    "EnableKinesisStreamingConfiguration": {}
}
```

Confirm that Kinesis streaming is active on the Orders table using the following command.

```bash
aws dynamodb describe-kinesis-streaming-destination \
    --table-name Orders \
    --query "KinesisDataStreamDestinations[0].DestinationStatus"
```

The sample output will include the table name, the Kinesis data stream ARN and the streaming status.

```
"ACTIVE"
```
