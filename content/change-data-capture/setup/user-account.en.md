---
title: "Start: On your own"
date: 2019-12-02T07:05:12-08:00
weight: 10
chapter: true
---


::alert[Only complete this section if you are running the workshop on your own. If you are at an AWS hosted event (such as re\:Invent, Immersion Day, etc), go to :link[At an AWS hosted Event]{href="/event-driven-architecture/setup/start-here/aws-ws-event"}]

## Create a Cloud9 Environment

To complete the steps in these labs, you need an IAM role that has the privileges to create, update and delete AWS Cloud9 environments, Lambda functions, DynamoDB tables, IAM roles, Kinesis Data Streams and DynamoDB Streams

* Log into the AWS Management Console, go to the AWS Cloud9 service dashboard then select **Create environment**.

![Create Cloud9 environment](/static/images/change-data-capture/setup/cloud9-create-env.png)

* Give your new environment a name - **DynamoDB Labs** then provide an optional description for the environment.

![Name Cloud9 environment](/static/images/change-data-capture/setup/cloud9-name-env.png)

* Select **t2.small** as your instance type, leave all other fields as the default values then select **Create**.

![Select Cloud9 instance](/static/images/change-data-capture/setup/cloud9-select-ec2.png)

* Wait for creation of your Cloud9 environment to complete then select **Open** to launch your Cloud9 evironment.

![Launch Cloud9 environment](/static/images/change-data-capture/setup/cloud9-launch-env.png)

Start a command line terminal in Cloud9 and set up the `Region` and `Account ID` environment variables.

```bash
export REGION={your aws region} &&
export ACCOUNT_ID={your aws account ID}
```

Install jq on your AWS Cloud9 environment using the command below.

```bash
sudo yum install jq -y
```

::alert[*After completing the workshop, remember to complete the :link[Clean Up]{href="/change-data-capture/clean-up"} section to remove AWS resources that you no longer require.*]

Now that your environment is set up, continue on to the :link[2. Scenario Overview]{href="/change-data-capture/overview"}.  
