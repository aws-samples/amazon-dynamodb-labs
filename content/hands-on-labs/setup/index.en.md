---
title: "1. Getting Started"
date: 2021-04-21T07:33:04-05:00
weight: 10
chapter: true
---


In this chapter, we'll cover the prerequisites needed to get started with [Amazon DynamoDB](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html). You'll create DynamoDB tables and use a AWS Cloud9 envrironment to query these tables.

The deployment architecture that you will be building in this lab will look like the below.

![Final Deployment Architecture](/static/images/hands-on-labs/setup/dynamodb_lab_architecture.png)

## Prerequisites

To run this lab, you'll need an AWS account, and a user identity with access to the following services:

* Amazon DynamoDB
* Visual Studio Code Web Environment

You can use your own account, or an account provided through Workshop Studio Event Delivery as part of an AWS organized workshop.  Using an account provided by Workshop Studio is the easier path, as you will have full access to all AWS services, and the account will terminate automatically when the event is over.

### Account setup

#### Using an account provided to you by your lab instructor

If you are running this workshop using a link provided to you by your AWS instructor, please use that link and enter the access-code provided to you as part of the workshop. In the lab AWS account, the Visual Studio Code instance should already be provisioned. This should be available at the "Event Output" section in your Workshop studio URL. 

![CloudFormation parameters](/static/images/common/on-your-own-cf-03.png)

#### Using your own AWS account

If you are using your own AWS account, be sure you have access to create and manage resources in Amazon DynamoDB and EC2 instance.

*After completing the workshop, remember to complete the [cleanup](/hands-on-labs/cleanup.html) section to remove any unnecessary AWS resources.*