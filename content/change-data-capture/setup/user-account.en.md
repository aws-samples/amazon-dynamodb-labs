---
title: "Start: On your own"
date: 2019-12-02T07:05:12-08:00
weight: 10
chapter: true
---


::alert[These setup instructions are identitical for LADV, LHOL, LBED, LMR, and LGME - all of which use the same Visual Studio Code template. Only complete this section once, and only if you're running it on your own account.]{type="warning"}

::alert[Only complete this section if you are running the workshop on your own. If you are at an AWS hosted event (such as re\:Invent, Immersion Day, etc), go to :link[At an AWS hosted Event]{href="/hands-on-labs/setup/aws-ws-event"}]

## Launch the CloudFormation stack
::alert[During the course of the lab, you will make DynamoDB tables that will incur a cost that could approach tens or hundreds of dollars per day. Ensure you delete the DynamoDB tables using the DynamoDB console, and make sure you delete the CloudFormation stack as soon as the lab is complete.]

1. **[Deprecated]** - Launch the CloudFormation template in US West 2 to deploy the resources in your account: [![CloudFormation](/static/images/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=us-west-2#/stacks/new?stackName=DynamoDBID&templateURL=:param{key="design_patterns_s3_lab_yaml"})  

1. *Optionally, download [the YAML template](https://s3.amazonaws.com/amazon-dynamodb-labs.com/assets/vscode.yaml) from our GitHub repository and launch it your own way*

1. Click *Next* on the first dialog.

1. Provide a CloudFormation stack name.

1. In the Parameters section, note the *AllowedIP** contains a default IP Address, if you want to access the instance via SSH obtain your own public IP address. Ensure to add the `/32` network mask at the end. Do not modify any other parameter and click *Next*.

![CloudFormation parameters](/static/images/common/on-your-own-cf-01.png)

6. Scroll to the bottom and click *Next*, and then review the *Template* and *Parameters*. When you are ready to create the stack, scroll to the bottom, check the box acknowledging the creation of IAM resources, and click *Create stack*.

![CloudFormation parameters](/static/images/common/on-your-own-cf-02.png)
  
  The stack will create a Visual Studio Code EC2 instance, a role for the instance, and a role for the AWS Lambda function used later on in the lab. The CloudFormation template will create a set of folders that can be used to execute individually the lab modules presented in this guide. 


::alert[*After completing the workshop, remember to complete the :link[Clean Up]{href="/change-data-capture/clean-up"} section to remove AWS resources that you no longer require.*]

Now that your environment is set up, continue on to the :link[2. Scenario Overview]{href="/change-data-capture/overview"}.  
