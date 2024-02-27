---
title: "Configure OpenSearch Service Permissions"
menuTitle: "Configure OpenSearch Service Permissions"
date: 2024-02-23T00:00:00-00:00
weight: 30
---
The OpenSearch Service Domain deployed by the CloudFormation Template uses Fine-grained access control. Fine-grained access control offers additional ways of controlling access to your data on Amazon OpenSearch Service. In order to configure integrations between OpenSearch Service, DynamoDB, and Bedrock certain OpenSearch Service permissions will need to be mapped to the IAM Role being used.

Links to the OpenSearch Dashboards, credentials, and necissary values are provided in the Outputs of the CloudFormation Template. It is recommended that you leave Outputs open in one browser tab to easily refer to while following through the lab.

In a production environment as a best practice, you would configure roles with the least privilege required. For simplicity in this lab, we will use the "all_access" OpenSearch Service role.

::alert[_Do not continue unless the CloudFormation Template has finished deploying._]

 1. Open the "Outputs" tab of your recently deployed Stack in the CloudFormation Console.
   ![CloudFormation Outputs](/static/images/ddb-os-zetl3.jpg)
 1. Open the link for OSDashboardsURL in a new tab.
 1. Login to Dashboards with the username and password provided in CloudFormation Outputs. The attributes named "OSMasterUserName" and "OSMasterUserPassword" provide the correct values.
  ![OpenSearch Service Dashboards](/static/images/ddb-os-zetl4.jpg)
 1. Open the top left menu and select "Security".
  ![Security Settings](/static/images/ddb-os-zet5.jpg) 
 1. Open the "Roles" tab, then click on the "all_access" role.
  ![Roles Settings](/static/images/ddb-os-zet6.jpg) 
 1. Open the "Mapped users" tab, then select "Manage mapping".
  ![Mapping Settings](/static/images/ddb-os-zet7.jpg)
 1. In the "Backend roles" field, enter the Arn provided in the CloudFormation Stack Outputs. The attribute named "Role" provides the correct Arn. Click "Map".
  ![ Settings](/static/images/ddb-os-zet8.jpg)
 1. Verify that the "all_access" Role now has a "Backend role" listed.
  ![ Settings](/static/images/ddb-os-zet9.jpg)
