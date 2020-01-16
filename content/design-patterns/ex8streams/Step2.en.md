+++
title = "Step 2 - Review the IAM policy for the IAM role"
date = 2019-12-02T12:34:06-08:00
weight = 2
+++



We have pre-created the IAM role DDBReplicationRole that will be used in this lab. This IAM role will allow the AWS Lambda service to read from the DynamoDB Streams. Review the following policy which is attached to the IAM role DDBReplicationRole:
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

Here are some of the permissions granted to AWS Lambda function in the policy:

- The Lambda function can put and delete items only in the logfile_replica table
- Log events will be published to CloudWatch Logs (but in this lab they are not available to students)
