+++
title = "Configure MySQL Environment"
menuTitle = "Configure MySQL Environment"
date = 2021-04-25T07:33:04-05:00
weight = 20

+++
This chapter will create source environment on AWS as discussed during Exercise Overview.
The CloudFormation template used below will create Source VPC, EC2 hosting MySQL server, IMDb database and load IMDb public dataset into 6 tables.

1. Launch the CloudFormation template in US East 1 to deploy the resources in your account:
  <a href="https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/new?stackName=rdbmsmigration&templateURL={{% siteparam "lhol_migration_setup_yaml" %}}" target="_blank"><img src="/images/cloudformation-launch-stack.png" alt="CloudFormation"/></a>
  *Optionally, download [the YAML template]({{% siteparam "lhol_migration_setup_yaml" %}}) and launch it your own way in the [CloudFormation Console](https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/create/template)*
 4. Click Next
 5. Confirm the Stack Name *rdbmsmigration* and update parameters if necessary (leave the default options if at all possible)
   ![Final Deployment Architecture](/images/migration6.jpg)
 6. Click “Next” twice then check “I acknowledge that AWS CloudFormation might create IAM resources with custom names.”
 7. Click "Submit"
 8. The CloudFormation stack will take about 5 minutes to build the environment
  ![Final Deployment Architecture](/images/migration7.jpg)
 9. Go to [EC2 Dashboard](https://console.aws.amazon.com/ec2/v2/home?region=us-east-1#Instances:)  and ensure the Status check column is 2/2 checks passed before moving to the next step.
 ![Final Deployment Architecture](/images/migration8.jpg)


{{% notice note %}}
_Do not continue unles the MySQL instance is passing both health checks, 2/2._
{{% /notice %}}