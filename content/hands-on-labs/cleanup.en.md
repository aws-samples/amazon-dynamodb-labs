+++
title = "Cleanup"
chapter = true
description = "Cleanup Resources Created During Lab"

weight = 1000
+++

If you used an account provided by Workshop Studio Event Delivery, you do not need to do any cleanup. The account terminates when the event is over.

If you used your own account, please remove the following resources:

* The four DynamoDB tables created in the Getting Started section of the lab:

```bash
aws dynamodb delete-table \
    --table-name ProductCatalog

aws dynamodb delete-table \
    --table-name Forum

aws dynamodb delete-table \
    --table-name Thread

aws dynamodb delete-table \
    --table-name Reply
```

* The Cloudformation template that was launched during the getting started section.  Navigate to the Cloudformation console, select the `dynamodb-labs` stack and click `Delete`.

![Cleanup Delete dynamodb-labs CFN Stack](/images/hands-on-labs/dynamodb-labs-cfn-delete-stack.png)

This should wrap up the cleanup process.
