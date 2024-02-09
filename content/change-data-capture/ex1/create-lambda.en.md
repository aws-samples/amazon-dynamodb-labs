---
title: "Create Lambda Function"
date: 2023-12-01T00:00:00-00:00
weight: 115
chapter: true
---

Create a lambda function to copy changed records from the Orders DynamoDB streams to the OrdersHistory table.

1. Open the **AWS Management Console** and go to the **Lambda Service** dashboard.
2. In the **Functions** section, click on **Create function**.
3. Select **Author from scratch**.
4. Set **create-order-history-ddbs** as the function name.
5. Select a version of **Python** as the runtime.

![AWS Lambda function creation wizard](/static/images/change-data-capture/ex1/set-name.png)  

6. Expand the **Change default execution role** section.
7. Select **Create a new role from AWS policy templates**.
8. Set **create-order-history-ddbs-execution-role** as the role name.
9. Select the **Simple microservice permissions** from the **Policy templates** options menu.

![AWS Lambda function creation wizard](/static/images/change-data-capture/ex1/set-permissions.png) 

10. Click **Create function** and wait to be redirected to the AWS Lambda console for your newly created function.

11. Replace the content of **lambda_function.py** with the function code below.

```python
import os
import boto3
import datetime
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.data_classes.dynamo_db_stream_event import (
    DynamoDBStreamEvent,
    DynamoDBRecordEventName
)
from botocore.exceptions import ClientError

table_name = os.getenv("ORDERS_HISTORY_DB")
logger = Logger()

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(table_name)


def store_history_record(old_item_image):
    logger.debug({"operation": "store_history_record", "old_image": old_item_image})

    # Set a value for the partition key - pk, and sort key - sk; for the OrdersHistory table
    # before writing the record to the OrdersHistory table.
    pk = old_item_image["id"]
    sk = str(datetime.datetime.now())
    old_item_image["pk"] = pk
    old_item_image["sk"] = sk

    try:
        response = table.put_item(
            Item=old_item_image
        )
        logger.debug({"operation": "table.put_item", "response": response})
    except ClientError as err:
        logger.error({"operation": "store_history_record", "details": err})
        raise Exception(err)


def lambda_handler(event, context):
    logger.debug({"operation": "lambda_handler", "event": event, "context": context})
    event: DynamoDBStreamEvent = DynamoDBStreamEvent(event)

    for record in event.records:
        if record.event_name == DynamoDBRecordEventName.MODIFY or record.event_name == DynamoDBRecordEventName.REMOVE:
            logger.debug({"record": record})
            store_history_record(record.dynamodb.old_image)

```

This lambda function receives events from DynamoDB streams and writes new items to a DynamoDB table i.e. the OrdersHistory table.

Since we only need to record changes to items on the Orders table, the lambda function is set to process only stream events for modified and deleted items from the Orders table.

12. Deploy the code changes to your function by selecting **Deploy**.

![AWS Lambda function creation wizard](/static/images/change-data-capture/ex1/deploy-code.png)

Do not execute the lambda function you created yet. Additional configuration is required for the set up to work correctly. You will update your lambda function configuration in the next step.
