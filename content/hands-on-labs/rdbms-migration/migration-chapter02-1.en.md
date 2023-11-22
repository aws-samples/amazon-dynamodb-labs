---
title: "Create DMS Resources"
menuTitle: "Create DMS Resources"
date: 2021-04-25T07:33:04-05:00
weight: 25
---

Let's create the DMS resources for the workshop.

1.  Go to IAM console > Roles > Create Role
2.  Under “Select trusted entity” select “AWS service” then under “Use case” select “DMS” from the pulldown list and click the “DMS” radio button. Then click “Next”
3.  Under “Add permissions” use the search box to find the “AmazonDMSVPCManagementRole” policy and select it, then click “Next”
5.  Under “Name, review, and create” add the role name as dms-vpc-role and click Create role

::alert[_Do not continue unless you have made the IAM role._]

1. Launch the CloudFormation template in US East 1 to deploy the resources in your account:
  <a href="https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/new?stackName=dynamodbmigration&templateURL={{% siteparam "lhol_migration_dms_setup_yaml" %}}" target="_blank"><img src="/images/cloudformation-launch-stack.png" alt="CloudFormation"/></a>
  *Optionally, download [the YAML template]({{% siteparam "lhol_migration_dms_setup_yaml" %}}) and launch it your own way in the [CloudFormation Console](https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/create/template)*
9.  Click Next
10. Confirm the Stack Name *dynamodbmigration* and keep the default parameters (modify if necessary)
    ![Final Deployment Architecture](/static/images/migration18.jpg)
11. Click “Next” twice
12. Check “I acknowledge that AWS CloudFormation might create IAM resources with custom names.”
1.  Click Submit. The CloudFormation template will take about 15 minutes to build a replication environment. You should continue the lab while the stack creates in the background.
    ![Final Deployment Architecture](/static/images/migration19.jpg)

::alert[_Do not wait for the stack to complete creation._ **Please continue the lab and allow it to create in the background.**]
