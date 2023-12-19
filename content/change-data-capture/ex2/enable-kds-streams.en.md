---
title: "Enable Kinesis Data Streams"
date: 2023-12-01T00:00:00-00:00
weight: 205
chapter: true
---

Disable DynamoDB streams for the **Orders** table using the AWS CLI commands below.

```bash
aws dynamodb update-table \
    --table-name Orders \
    --stream-specification \
        StreamEnabled=false > output.log
```

Confirm that DynamoDB streams has been disabled using the AWS CLI commands below.

```bash
aws dynamodb describe-table --table-name Orders | jq '.Table | .TableStatus, .StreamSpecification.StreamEnabled'
```

An output of **ACTIVE** and **null** as shown below confirms that the DynamoDB table is active but streams has been disabled.

```
"ACTIVE"
null
```

Create a Kinesis data stream named **Orders** using the following command.
```bash
aws kinesis create-stream --stream-name Orders --shard-count 2
```
Confirm that the stream is active using the following command.

```bash
aws kinesis describe-stream --stream-name Orders | jq '.StreamDescription.StreamStatus'
```

Sample output:

```
"ACTIVE"
```

Enable Kinesis streaming for the Orders DynamoDB table using following command.

```bash
aws dynamodb enable-kinesis-streaming-destination \
    --table-name Orders \
    --stream-arn arn:aws:kinesis:${REGION}:${ACCOUNT_ID}:stream/Orders
```

Confirm that Kinesis streaming is active on the Orders table using the following command.

```bash
aws dynamodb describe-kinesis-streaming-destination \
    --table-name Orders | \
    jq '.TableName, .KinesisDataStreamDestinations[].StreamArn, .KinesisDataStreamDestinations[].DestinationStatus'
```

The sample output will include the table name, the Kinesis data stream ARN and the streaming status.

```
"Orders"
"arn:aws:kinesis:{REGION}:{ACCOUNT_ID}:stream/Orders"
"ACTIVE"
```
