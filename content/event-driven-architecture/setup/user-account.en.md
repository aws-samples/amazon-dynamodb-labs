---
title: "On your own"
date: 2019-12-02T07:05:12-08:00
weight: 5
chapter: true
pre: "<b>Start: </b>"
---


::alert[Only complete this section if you are running the workshop on your own. If you are at an AWS hosted event (such as re:Invent, Immersion Day, etc), go to [At an AWS hosted Event]({{< ref "event-driven-architecture/setup/start-here/aws-ws-event">}})]
## Launch the CloudFormation stack
::alert[During the course of the lab, you will make DynamoDB tables that will incur a cost that could approach tens or hundreds of dollars per day. Ensure you delete the DynamoDB tables using the DynamoDB console, and make sure you delete the CloudFormation stack as soon as the lab is complete.]{type="warning"}

1. Launch the CloudFormation template in US East 1 to deploy the resources in your account:
  <a href="https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/new?stackName=amazon-dynamodb-labs&templateURL={{% siteparam "event_driven_architecture_lab_yaml" %}}" target="_blank"><img src="/images/cloudformation-launch-stack.png" alt="CloudFormation"/></a>
  *Optionally, download [the YAML template]({{% siteparam "event_driven_architecture_lab_yaml" %}}) and launch it your own way*

1. Click *Next* on the first dialog.

1. Scroll to the bottom and click *Next*, and then review the *Template*. When you are ready to create the stack, scroll to the bottom, check the box acknowledging the creation of IAM resources, and click *Create stack*.
![CloudFormation parameters](/static/images/awsconsole2.png)
  The stack will create DynamoDB tables, Lambda functions, Kinesis streams, and IAM roles and policies which will be used later on in the lab.

1. After the CloudFormation stack is `CREATE_COMPLETE`, [continue onto the overview]({{< ref "event-driven-architecture/ex1overview" >}}).  
