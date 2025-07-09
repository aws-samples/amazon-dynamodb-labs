---
title: "Configure Lambda Function"
date: 2023-12-01T00:00:00-00:00
weight: 220
chapter: true
---

Configure your lambda function to copy changed records from the Orders Kinesis Data Stream to the OrdersHistory table.

1. Go to the IAM dashboard on the AWS Management Console and inspect the IAM policy, i.e. **AWSLambdaMicroserviceExecutionRole...**, created when you created the **create-order-history-kds** lambda function.

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "dynamodb:DeleteItem",
                "dynamodb:GetItem",
                "dynamodb:PutItem",
                "dynamodb:Scan",
                "dynamodb:UpdateItem"
            ],
            "Resource": "arn:aws:dynamodb:{aws-region}:{aws-account-id}:table/*"
        }
    ]
}
```

2. Update the policy statement by editing and replacing the existing policy using the following IAM policy statement. 

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "kinesis:DescribeStream",
                "kinesis:GetRecords",
                "kinesis:GetShardIterator",
                "kinesis:ListStreams"
            ],
            "Resource": "arn:aws:kinesis:{aws-region}:{aws-account-id}:stream/Orders"
        },
        {
            "Effect": "Allow",
            "Action": "dynamodb:PutItem",
            "Resource": "arn:aws:dynamodb:{aws-region}:{aws-account-id}:table/OrdersHistory"
        },
        {
            "Effect": "Allow",
            "Action": "sqs:SendMessage",
            "Resource": "arn:aws:sqs:{aws-region}:{aws-account-id}:orders-kds-dlq"
        }
    ]
}
```

::alert[Replace **{aws-region}** and **{aws-account-id}** in the policy statement above with your AWS region and account ID respectively.]

3. Select **Layers** then select **Add a Layer**.

![AWS Lambda function console](/static/images/change-data-capture/ex2/select-layer.png)

![AWS Lambda function console](/static/images/change-data-capture/ex2/add-layer.png)

4. Select **Specify an ARN**, enter the Lambda Layer ARN below.

```bash
arn:aws:lambda:{aws-region}:017000801446:layer:AWSLambdaPowertoolsPythonV2:58
```

5. Click **Verify** then select **Add**. 

![AWS Lambda function console](/static/images/change-data-capture/ex1/specify-layer.png)

::alert[Replace {aws-region} with ID for the AWS region that you are currently working on.]

6. Go to the configuration section of the lambda console editor. Select **Environment variables** then select **Edit**.

![AWS Lambda function console](/static/images/change-data-capture/ex1/edit-env-var.png) 

7. Add a new environment variable called **ORDERS_HISTORY_DB** and set its value to **OrdersHistory**.

![AWS Lambda function console](/static/images/change-data-capture/ex1/new-env-var.png) 

8. Go to the configuration section of the lambda console editor. Select **Triggers** then select **Add trigger**.
9. Select **Kinesis** as the trigger source.
10. Select the **Orders** DynamoDB table.
11. Set the **Batch size** to **10** and leave all other values unchanged.

![AWS Lambda function console](/static/images/change-data-capture/ex2/trigger.png) 

12. Click **Additional settings** to expand the section.
13. Provide the ARN of the orders-kds-dlq SQS queue you created earlier.
14. Set the Retry attempts to 3.

![AWS Lambda function console](/static/images/change-data-capture/ex2/trigger-settings.png) 

15. Select **Add**.
