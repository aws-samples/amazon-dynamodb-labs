---
title: "Enable DynamoDB Streams"
date: 2023-12-01T00:00:00-00:00
weight: 105
chapter: true
---

When [enabling DynamoDB streams](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Streams.html#Streams.Enabling) on a table, you can choose to record one of the following.

* **Key attributes** only - the key attributes of the item being updated
* **New image** - the new image of an item after it is updated
* **Old image** - the original image of an item before it was updated
* **New and old images** - the before and after image of an item following an update. 

Since the requirement for this scenario is to retain only the current view of orders on the Orders table, you need to set the DynamoDB stream for the table to only hold the **old image** of items when updates are performed. The **new image** does not need to be written to the stream since it is not required.

Enable DynamoDB streams on the Orders table by running the AWS CLI command below.

```bash
aws dynamodb update-table \
    --table-name Orders \
    --stream-specification \
        StreamEnabled=true,StreamViewType=OLD_IMAGE > output.log
```
Confirm that DynamoDB streams has been enabled using the AWS CLI commands below.

```bash
aws dynamodb describe-table --table-name Orders \
    | jq '.Table | .TableStatus, .StreamSpecification.StreamEnabled, .LatestStreamArn'
```

The output would show the table status, whether DynamoDB streams is enabled for the table and the Amazon resource name (ARN) for the tables stream as shown below.

```
"ACTIVE"
true
"arn:aws:dynamodb:{REGION}:{ACCOUNT_ID}:table/Orders/stream/YYYY-MM-DDThh:mm:ss.SSS"
```
