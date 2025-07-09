---
title: "Create Dead Letter Queue"
date: 2023-12-01T00:00:00-00:00
weight: 210
chapter: true
---

If the lambda function is not able to successfully process any record it receives from Amazon Kinesis, the Lambda service should write the metadata for the error record to a dead letter queue (DLQ) so the reason for the failure can be investigated and resolved. 

So create an [Amazon SQS Dead Letter Queue](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-dead-letter-queues.html) named **orders-kds-dlq** for your lambda function trigger using the AWS CLI command below.

```bash
aws sqs create-queue --queue-name orders-kds-dlq
```

Sample output:

```
{
    "QueueUrl": "https://sqs.{aws-region}.amazonaws.com/{aws-account-id}/orders-kds-dlq"
}
```

As before you will need the queue ARN. Use the below command, modifying the queue URL after *--queue-url* to match the result of the previous command.

```bash
aws sqs get-queue-attributes --attribute-names "QueueArn" --query 'Attributes.QueueArn' --output text \
--queue-url "https://sqs.{aws-region}.amazonaws.com/{aws-account-id}/orders-kds-dlq"
```