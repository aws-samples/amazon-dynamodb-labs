+++
title = "Configure the Environment"
menuTitle = "Configure the Environment"
date = 2021-04-25T07:33:04-05:00
weight = 20

+++
The following steps should be executed to deploy the emulated source environment in AWS account:

 1. Download the [CloudFormation](/files/hands-on-labs/migration-env-setup.yaml) template
 2. Open [CloudFormation](https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/create/template), click on Create Stack and select With new resources (standard)
 3. Select Template source as Upload a template file and choose the downloaded yaml file
   ![Final Deployment Architecture](/images/migration5.jpg)
 4. Click Next
 5. Provide Stack Name and Update Parameters
   ![Final Deployment Architecture](/images/migration6.jpg)
 6. Click Next
 7. Click Create stack
 8. The CloudFormation template will take 15-20 minutes to build the envirorment
  ![Final Deployment Architecture](/images/migration7.jpg)
 9. Go to [EC2 Dashboard](https://console.aws.amazon.com/ec2/v2/home?region=us-east-1#Instances:)  and ensure Status check column is 2/2 checks passed before moving to next step.
 ![Final Deployment Architecture](/images/migration8.jpg)
