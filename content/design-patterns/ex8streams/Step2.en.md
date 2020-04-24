+++
title = "Step 2 - Review the AWS IAM policy for the IAM role"
date = 2019-12-02T12:34:06-08:00
weight = 2
+++


We have pre-created the IAM role `DDBReplicationRole` that will be used as the [AWS Lambda Execution Role](https://docs.aws.amazon.com/lambda/latest/dg/lambda-intro-execution-role.html). This IAM role allows provides several permissions to the AWS Lambda function we will need to replicate data.

Review the following policy which is attached to the IAM role `DDBReplicationRole`.
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": [
                "dynamodb:DescribeStream",
                "dynamodb:GetRecords",
                "dynamodb:GetShardIterator",
                "dynamodb:ListStreams"
            ],
            "Resource": [
                "*"
            ],
            "Effect": "Allow"
        },
        {
            "Action": [
                "dynamodb:DeleteItem",
                "dynamodb:PutItem"
            ],
            "Resource": [
                "*"
            ],
            "Effect": "Allow"
        },
        {
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": [
                "*"
            ],
            "Effect": "Allow"
        }
    ]
}
```

These are some of the permissions granted to the Lambda function in the policy:

-  The AWS Lambda service should have the ability to call DynamoDB Streams and retrieve records from the stream.
```json
{
    "Action": [
        "dynamodb:DescribeStream",
        "dynamodb:GetRecords",
        "dynamodb:GetShardIterator",
        "dynamodb:ListStreams"
    ],
    "Resource": [
        "*"
    ],
    "Effect": "Allow"
}
```

- The Lambda function can put and delete items only in the `logfile_replica` table.
```json
{
    "Action": [
        "dynamodb:DeleteItem",
        "dynamodb:PutItem"
    ],
    "Resource": [
        "*"
    ],
    "Effect": "Allow"
}
```
- Log events are published to Amazon CloudWatch Logs (but in this lab they are not available).
```json
{
    "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
    ],
    "Resource": [
        "*"
    ],
    "Effect": "Allow"
}
```
