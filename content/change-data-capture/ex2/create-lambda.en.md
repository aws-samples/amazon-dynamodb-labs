---
title: "Create Lambda Function"
date: 2023-12-01T00:00:00-00:00
weight: 215
chapter: true
---

Create a lambda function to copy changed records from the Orders DynamoDB streams to the OrdersHistory table.

1. Open the **AWS Management Console** and go to the **Lambda** Service dashboard.
2. In the **Functions** section, click on **Create function**.
3. Select **Author from scratch**.
4. Set **create-order-history-kds** as the function name.
5. Select a version of **Python** as the runtime.
6. Expand the **Change default execution role** section.
7. Select **Create a new role from AWS policy templates**.
8. Set **create-order-history-kds-execution-role** as the role name.
9. Select the **Simple microservice permissions** from the **Policy templates** options menu.
10. Click **Create function** and wait to be redirected to the AWS Lambda console for your newly created function.
11. Replace the content of **lambda_function.py** with the function code below.

```python
import os
import boto3
import datetime
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.data_classes import event_source, KinesisStreamEvent
from botocore.exceptions import ClientError

table_name = os.getenv("ORDERS_HISTORY_DB")
logger = Logger()

client = boto3.client('dynamodb')


def store_history_record(old_order_image):
    logger.debug({"Saving order history"})

    # Set a value for the partition key - pk, and sort key - sk; for the OrderHistory table
    # before writing the record to the OrderHistory table.
    pk = old_order_image["id"]
    sk = str(datetime.datetime.now())
    old_order_image["pk"] = pk
    old_order_image["sk"] = {
        "S": sk
    }
    logger.debug({"old_image": old_order_image})

    try:
        response = client.put_item(
            TableName=table_name,
            Item=old_order_image
        )
        logger.debug({"operation": "table.put_item", "response": response})
    except ClientError as err:
        logger.error({"operation": "store_history_record", "details": err})
        raise Exception(err)


@event_source(data_class=KinesisStreamEvent)
def lambda_handler(event: KinesisStreamEvent, context):
    logger.debug({"operation": "lambda_handler", "event": event, "context": context})

    kinesis_record = next(event.records).kinesis
    data = kinesis_record.data_as_json()
    if data["eventName"] == "MODIFY" or data["eventName"] == "REMOVE":
        logger.debug({"data": data})
        if "dynamodb" in data:
            if "OldImage" in data["dynamodb"]:
                store_history_record(data["dynamodb"]["OldImage"])

```

::::expand{header="Expand this section for an explanation of the function code"}

| Line Number |  Description  |
|:-------------------- | :------------------ |
| 8 - 11 | Get the Orders History DynamoDB table name from an environment variable, instantiate a logger for the lambda function then create a boto3 client for interacting with DynamoDB tables. |
| 19 - 24 | Create a new item for the Orders History table using an old image of an item updated on the Orders table. Set the partition key for the new item to the `id` of the updated order then set the sort key for the new item to the current time. |
| 27 - 35 | Write the new item to the Orders History table. Raise an exception if the item is not successfully written to the table. |
| 42 - 48 | Process old images of update item event and delete item event received from the Orders Kinesis Data stream. |

::::

This lambda function receives events from the Orders Kinesis data stream and writes them to the OrdersHistory dynamoDB table.

Since we only need to record changes to items on the Orders table, the lambda function is set to process only Kinesis stream events for modified and deleted items from the Orders table.

12. Deploy the code changes to your function by selecting **Deploy**.

![AWS Lambda function creation wizard](/static/images/change-data-capture/ex2/deploy-code.png)
