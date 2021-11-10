+++
title = "Configure the Environment"
menuTitle = "Configure the Environment"
date = 2021-04-25T07:33:04-05:00
weight = 20

+++
The following steps should be executed to deploy the emulated source environment in AWS account:

 1. Download the [CloudFormation](/files/hands-on-labs/migration-env-setup.yaml) template
 2. Sign in to your AWS Account [AWS Console](https://console.aws.amazon.com/) using an account with administrative privileges
 3. Select N. Virginia Region (us-east-1)
 ![Final Deployment Architecture](/images/migration1.jpg)
 4. Open CloudFormation, click on Create Stack and select With new resources (standard)
  ![Final Deployment Architecture](/images/migration2.jpg)
 5. Select Template source as Upload a template file and choose the downloaded yaml file
 6. Click Next
 7. Provide Stack Name and Update Parameters
 8. Click Next
 9. Click Create stack
10. The CloudFormation template will take 15-20 minutes to build the envirorment.  
