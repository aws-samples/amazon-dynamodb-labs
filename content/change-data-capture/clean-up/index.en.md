---
title: "5. Summary & Clean Up"
date: 2023-12-01T00:00:00-00:00
weight: 20
chapter: true
---

Congratulations! You have made it to the end of the workshop.

In this workshop you explored capturing item level changes on a DynamoDB table using DynamoDB Streams and Kinesis Data Streams. In this instance, you wrote the previous version of updated items to a different DynamoDB table. By applying these same techniques, you can build complex event driven solutions that are triggered by changes to items you have stored on DynamoDB.

If you used an account provided by Event Engine, you do not need to do any cleanup. The account terminates when the event is over.

If you used your own account, please remove the following resources:

* The Lambda Function Event Source Mappings:

```bash
uuid=`aws lambda list-event-source-mappings \
    --function-name create-order-history-kds | jq '.EventSourceMappings[].UUID' --raw-output`
aws lambda delete-event-source-mapping --uuid ${uuid} > output.log
uuid=`aws lambda list-event-source-mappings \
    --function-name create-order-history-ddbs | jq '.EventSourceMappings[].UUID' --raw-output`
aws lambda delete-event-source-mapping --uuid ${uuid} >> output.log
```

* The AWS Lambda functions created during the labs:

```bash
aws lambda delete-function --function-name create-order-history-ddbs >> output.log
aws lambda delete-function --function-name create-order-history-kds >> output.log
```  

* The AWS Kinesis data stream created during the labs:

```bash
aws kinesis delete-stream --stream-name Orders >> output.log
```

* The Amazon DynamoDB tables created in the Getting Started section of the lab:

```bash
aws dynamodb delete-table --table-name Orders >> output.log
aws dynamodb delete-table --table-name OrdersHistory >> output.log
```

* The Amazon SQS queues created during the labs:

```bash
aws sqs delete-queue --queue-url https://sqs.${REGION}.amazonaws.com/${ACCOUNT_ID}/orders-ddbs-dlq
aws sqs delete-queue --queue-url https://sqs.${REGION}.amazonaws.com/${ACCOUNT_ID}/orders-kds-dlq
```

* The IAM policies attached to the IAM execution roles you created:

![Delete IAM Policies](/static/images/change-data-capture/cleanup/delete-policies-one.png)

![Delete IAM Policies](/static/images/change-data-capture/cleanup/delete-policies-two.png)

* The AWS IAM execution roles created for the lambda functions:

![Delete IAM Roles](/static/images/change-data-capture/cleanup/delete-roles.png)

This should wrap up the cleanup process.