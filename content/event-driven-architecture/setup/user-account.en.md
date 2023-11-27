---
title: "Start: On your own"
date: 2019-12-02T07:05:12-08:00
weight: 5
chapter: true
---


::alert[Only complete this section if you are running the workshop on your own. If you are at an AWS hosted event (such as re\:Invent, Immersion Day, etc), go to :link[At an AWS hosted Event]{href="/event-driven-architecture/setup/start-here/aws-ws-event"}]
## Launch the CloudFormation stack
::alert[During the course of the lab, you will make DynamoDB tables that will incur a cost that could approach tens or hundreds of dollars per day. Ensure you delete the DynamoDB tables using the DynamoDB console, and make sure you delete the CloudFormation stack as soon as the lab is complete.]{type="warning"}

1. Launch the CloudFormation template in US West 2 to deploy the resources in your account: [![CloudFormation](/static/images/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=us-west-2#/stacks/new?stackName=amazon-dynamodb-labs&templateURL=:param{key="event_driven_architecture_lab_yaml"})  
    1. *Optionally, download [the YAML template](:param{key="event_driven_architecture_lab_yaml"}) and launch it your own way*

1. Click *Next* on the first dialog.

1. Scroll to the bottom and click *Next*, and then review the *Template*. When you are ready to create the stack, scroll to the bottom, check the box acknowledging the creation of IAM resources, and click *Create stack*.
![CloudFormation parameters](/static/images/awsconsole2.png)
  The stack will create DynamoDB tables, Lambda functions, Kinesis streams, and IAM roles and policies which will be used later on in the lab.

1. After the CloudFormation stack is `CREATE_COMPLETE`, :link[continue onto the overview]{href="/event-driven-architecture/ex1overview"}.  



