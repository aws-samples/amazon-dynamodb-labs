+++
title = "Environment Set up"
menutitle="Set Up"
date = 2021-04-21T07:39:31-05:00
weight = 12
+++

{{% notice note %}}
_These instructions are for users running the lab in their own AWS account. If you are part of a workshop, check the AWS Cloud9 console in the correct region for a running environment named "DynamoDBC9" before you follow these instructions. You may not need to launch the template._
{{% /notice %}}

Download this [Cloud Formation Template](/files/hands-on-labs/dynamodb-labs-vpc.yaml) to your local machine.

You'll now create a stack in your AWS environment using this template. The deployed stack will contain the following.

* 1 Public Subnet
* 3 Private Subnets
* AWS Cloud9 Envrionment deployed in the Public Subnet

### Creating the Stack

Navigate to [Cloud Formation console](https://console.aws.amazon.com/cloudformation/home) using your AWS management [console](https://console.aws.amazon.com/). Choose *Create Stack* . If you have existing stacks, then select *With new resources (standard)* during this step.

On the Create stack page, choose *Upload a template file* option. Select *Choose file* and upload the .yaml file you downloaded earlier. Choose *Next*

![AWS Cloud Formation Template 1](/images/hands-on-labs/setup/dynamodb-labs-vpc-create-stack-1.png)

Give a name for the Stack and a ProjectTag. For this lab, we'll use `dynamodb-labs` as the name and `dynamodb-labs` as the tag. `dynamodb-labs` is the default value for tag.

![AWS Cloud Formation Template 2](/images/hands-on-labs/setup/dynamodb-labs-vpc-create-stack-2.png)

Choose *Next* in the following screen and then choose *Create Stack*.

The stack will be created in few minutes and you can view the VPC, public and private subnet IDs under the *Outputs* tab of your stack. You'll be using the VPC created by this Cloud Formation Template for the other sections of the lab.

![AWS Cloud Formation Template 3](/images/hands-on-labs/setup/dynamodb-labs-vpc-create-stack-3.png)
