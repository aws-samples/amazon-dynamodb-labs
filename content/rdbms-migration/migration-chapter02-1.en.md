---
title: "Create DMS Resources"
menuTitle: "Create DMS Resources"
date: 2021-04-25T07:33:04-05:00
weight: 25
---

Let's create the DMS resources for the workshop. First, we ensure if a DMS service role `dms-vpc-role` is already available. Then we need to deploy the DMS resources.

1.  Go to IAM console > Roles > Search for `dms-vpc-role`. If you see a role, skip to the CloudFormation stack deployment. Else, select **Create role** and follow next steps.
2.  Under **Select trusted entity** select **AWS service** then under **Use case** select **DMS** from the drop-down and click the **DMS** radio button. Then click **Next**
3.  Under **Add permissions** use the search box to find the `AmazonDMSVPCManagementRole` policy and select it, then click **Next**
5.  Under **Name, review, and create** add the role name as exactly `dms-vpc-role` and click **Create role**

::alert[_Do not continue unless you have made the IAM role._]

1. Launch the CloudFormation template in the workshop region to deploy the resources in your account: [![CloudFormation](/static/images/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home#/stacks/new?stackName=dynamodbmigration&templateURL=:param{key="lhol_migration_dms_setup_yaml"})  
    1. *Optionally, download [the YAML template](:param{key="lhol_migration_dms_setup_yaml"}) and launch it your own way*
9.  Click **Next**
10. Confirm the Stack name `dynamodbmigration` and keep the default parameters (modify if necessary)
    ![Final Deployment Architecture](/static/images/migration18.jpg)
11. Click **Next** twice
12. Check ***I acknowledge that AWS CloudFormation might create IAM resources with custom names***.
1.  Click **Submit**. The CloudFormation template will take about 15 minutes to build a replication environment. You should continue the lab while the stack creates in the background.
    ![Final Deployment Architecture](/static/images/migration19.jpg)

::alert[_Do not wait for the stack to complete creation._ **Please continue the lab and allow it to create in the background.**]


