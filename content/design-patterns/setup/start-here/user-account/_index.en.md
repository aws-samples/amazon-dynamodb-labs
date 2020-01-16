+++
title = "On your own"
date = 2019-12-02T07:05:12-08:00
weight = 4
chapter = true
pre = "<b>Start: </b>"
+++


{{% notice info %}}
Only complete this section if you are running the workshop on your own. If you are at an AWS hosted event (such as re:Invent, Immersion Day, etc), go to [At an AWS hosted Event]({{< ref "design-patterns/setup/start-here/aws-event">}})
{{% /notice %}}
## Create an AWS account

1. If you don’t already have an AWS account with Administrator access: [create one now by clicking here](https://aws.amazon.com/getting-started/)

1. Once you have an AWS account, ensure you are following the remaining workshop steps as an IAM user with administrator access to the AWS account: [Create a new IAM user to use for the workshop](https://console.aws.amazon.com/iam/home?#/users$new)

3. Enter the user details:
![Add user](/images/iam-1-create-user.png)

4. Attach the AdministratorAccess IAM Policy:
![Attach policy](/images/iam-2-attach-policy.png)

5. Click to create the new users:
![New user](/images/iam-3-create-user.png)

6. Take note of the login URL and save:
![Login URL](/images/iam-4-save-url.png)

7. Login using the URL and user credentials you just created:
![Sign in](/images/iam-signin.png)  

## Launch the CloudFormation stack
{{% notice warning %}}
During the course of the lab, you will make DynamoDB tables that will incur a cost that could approach tens or hundreds of dollars per day. Ensure you clean up the Amazon DynamoDB tables by deleting the CloudFormation stack as soon as the lab is complete.
{{% /notice %}}

1. Launch the CloudFormation template in US East 1 to deploy the resources in your account:
  <a href="https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/new?stackName=amazon-dynamodb-labs&templateURL={{% siteparam "design_patterns_s3_lab_yaml" %}}" target="_blank"><img src="/images/cloudformation-launch-stack.png" alt="CloudFormation"/></a>
  *Optionally, download [the YAML template]({{% siteparam "design_patterns_s3_lab_yaml" %}}) and launch it your own way*

1. Click *Next* on the first dialog.

1. In the Parameters section, note the default option for *VPCSelection* is `CreateNewVPC`. **The `CreateNewVPC` option has the highest chance of success**.  
    If you would like to use your default VPC, change this option to `Default`.  
    Leave the *WorkshopCodeURL* parameter unchanged and click *Next*
![CloudFormation parameters](/images/awsconsole1.png)

1. Scroll to the bottom and click *Next*, and then review the *Template* and *Parameters*. When you are ready to create the stack, scroll to the bottom, check the box acknowledging the creation of IAM resources, and click *Create stack*.
![CloudFormation parameters](/images/awsconsole2.png)
  The stack will create an EC2 lab instance, a role for the EC2 instance, and a role for the AWS Lambda function used later on in the lab.


1. After the CloudFormation stack is `CREATE_COMPLETE`, [continue onto Step 1]({{< ref "design-patterns/setup/Step1" >}}).  
  *If you chose `Default` in the *VPCSelection* dialog and your stack fails to create due to a VPC issue, re-create the stack and choose the default option `CreateNewVPC`*.
