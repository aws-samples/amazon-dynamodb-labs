---
title: "Prerequisites"
date: 2023-12-01T00:00:00-00:00
weight: 10
chapter: true
---

To run this lab, you'll need an AWS account, and a user identity with access to the following services:

* Amazon DynamoDB
* Amazon Kinesis
* AWS Lambda
* AWS Cloud9 Environment

You can use your own account, or an account provided through Event Engine as part of an AWS organized workshop.  Using an account provided by Event Engine is the easier path, as you will have full access to all AWS services, and the account will terminate automatically when the event is over.

### Account setup

#### Using an account provided to you by your lab instructor

If you are running this workshop using a link provided to you by your AWS instructor, please use that link and enter the access-code provided to you as part of the workshop. In the lab AWS account, the Cloud9 instance should already be provisioned. Please open the "AWS Cloud9" section of the AWS Management Console in the correct region and look for a lab instance called **DynamoDBC9**.

#### Using your own AWS account

If you are using your own AWS account, ensure you have access to create and manage resources in Amazon DynamoDB, AWS Lambda and AWS Cloud9 environment

Once you are in Cloud9, open a command line terminal and set up the `Region` and `Account ID` environment variables.

```bash
export REGION={your aws region} &&
export ACCOUNT_ID={your aws account ID}
```

Install jq on your AWS Cloud9 environment using the command below.

```bash
sudo yum install jq -y
```

::alert[*After completing the workshop, remember to complete the :link[Clean Up]{href="/change-data-capture/clean-up"} section to remove AWS resources that you no longer require.*]