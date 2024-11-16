---
title: "Configure MySQL Environment"
menuTitle: "Configure MySQL Environment"
date: 2021-04-25T07:33:04-05:00
weight: 20
---
This chapter will create source environment on AWS as discussed during Exercise Overview.
The CloudFormation template used below will create Source VPC, EC2 hosting MySQL server, IMDb database and load IMDb public dataset into 6 tables.

1. Launch the CloudFormation template in US West 2 to deploy the resources in your account: [![CloudFormation](/static/images/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=us-west-2#/stacks/new?stackName=rdbmsmigration&templateURL=:param{key="lhol_migration_setup_yaml"})  
    1. *Optionally, download [the YAML template](:param{key="lhol_migration_setup_yaml"}) and launch it your own way*
 4. Click Next
 5. Confirm the Stack Name *rdbmsmigration* and update parameters if necessary (leave the default options if at all possible)
   ![Final Deployment Architecture](/static/images/migration6.jpg)
 6. Click “Next” twice then check “I acknowledge that AWS CloudFormation might create IAM resources with custom names.”
 7. Click "Submit"
 8. The CloudFormation stack will take about 5 minutes to build the environment
  ![Final Deployment Architecture](/static/images/migration7.jpg)
 9. Go to [EC2 Dashboard](https://console.aws.amazon.com/ec2/v2/home?region=us-west-2#Instances:)  and ensure the Status check column is 2/2 checks passed before moving to the next step.
 ![Final Deployment Architecture](/static/images/migration8.jpg)


::alert[_Do not continue unless the MySQL instance is passing both health checks, 2/2._]


