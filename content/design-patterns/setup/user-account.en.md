---
title: "Start: On your own"
date: 2019-12-02T07:05:12-08:00
weight: 5
chapter: true
---

::alert[These setup instructions are identitical for LADV, LHOL, LMR, LBED, and LGME - all of which use the same Cloud9 template. Only complete this section once, and only if you're running it on your own account.]{type="warning"}

::alert[Only complete this section if you are running the workshop on your own. If you are at an AWS hosted event (such as re\:Invent, Immersion Day, etc), go to :link[At an AWS hosted Event]{href="/design-patterns/setup/aws-ws-event"}]

## Launch the CloudFormation stack
::alert[During the course of the lab, you will make DynamoDB tables that will incur a cost that could approach tens or hundreds of dollars per day. Ensure you delete the DynamoDB tables using the DynamoDB console, and make sure you delete the CloudFormation stack as soon as the lab is complete.]

1. Launch the CloudFormation template in US West 2 to deploy the resources in your account: [![CloudFormation](/static/images/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=us-west-2#/stacks/new?stackName=DynamoDBID&templateURL=:param{key="design_patterns_s3_lab_yaml"})  
    1. *Optionally, download [the YAML template](:param{key="design_patterns_s3_lab_yaml"}) and launch it your own way*

1. Click *Next* on the first dialog.

1. In the Parameters section, note the *Timeout* is set to zero. This means the Cloud9 instance will not sleep; you may want to change this manually to a value such as 60 to protect against unexpected charges if you forget to delete the stack at the end.  
    Leave the *WorkshopZIP* parameter unchanged and click *Next*
![CloudFormation parameters](/static/images/awsconsole1.png)

1. Scroll to the bottom and click *Next*, and then review the *Template* and *Parameters*. When you are ready to create the stack, scroll to the bottom, check the box acknowledging the creation of IAM resources, and click *Create stack*.
![CloudFormation parameters](/static/images/awsconsole2.png)
  The stack will create a Cloud9 lab instance, a role for the instance, and a role for the AWS Lambda function used later on in the lab. It will use Systems Manager to configure the Cloud9 instance.


1. After the CloudFormation stack is `CREATE_COMPLETE`, :link[continue onto Step 1]{href="/design-patterns/setup/Step1"}.  
