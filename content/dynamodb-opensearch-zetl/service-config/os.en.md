---
title: "Configure OpenSearch Service Permissions"
menuTitle: "Configure OpenSearch Service Permissions"
date: 2024-02-23T00:00:00-00:00
weight: 20
---
The OpenSearch Service Domain deployed by the CloudFormation Template uses Fine-grained access control. Fine-grained access control offers additional ways of controlling access to your data on Amazon OpenSearch Service. In order to configure integrations between OpenSearch Service, DynamoDB, and Bedrock certain OpenSearch Service permissions will need to be mapped to the IAM Role being used.

Links to the OpenSearch Dashboards, credentials, and necessary values are provided in the Outputs of the DynamoDBzETL [CloudFormation](https://console.aws.amazon.com/cloudformation/home?region=us-west-2#/stacks/) Template. It is recommended that you leave Outputs open in one browser tab to easily refer to while following through the lab.

In a production environment as a best practice, you would configure roles with the least privilege required. For simplicity in this lab, we will use the "all_access" OpenSearch Service role.

::alert[_Do not continue unless the CloudFormation Template has finished deploying._]

 1. Open the "Outputs" tab of the stack named `dynamodb-opensearch-setup` in the CloudFormation Console.

    ![CloudFormation Outputs](/static/images/ddb-os-zetl3.jpg)
 1. Open the link for SecretConsoleLink in a new tab. This will take you to the AWS Secrets Manager secret which contains the login information for OpenSearch. Click on the `Retrieve secret value` button to see the username and password for the OpenSearch Cluster.
 1. Return to the CloudFormation Console "Outputs" and open the link for **OSDashboardsURL** in a new tab.
 1. Login to Dashboards with the username and password provided in Secrets Manager.

    ![OpenSearch Service Dashboards](/static/images/ddb-os-zetl4.jpg)
1. When prompted to select your tenant, choose *Global* and click **Confirm**. Dismiss any pop ups.

    ![OpenSearch Service Dashboards](/static/images/ddb-os-zetl18.jpg)
 1. Open the top left menu and select **Security** under the *Management* section.

    ![Security Settings](/static/images/ddb-os-zetl5.jpg) 
 1. Open the "Roles" tab, then click on the "all_access" role.

    ![Roles Settings](/static/images/ddb-os-zetl6.jpg) 
 1. Open the "Mapped users" tab, then select "Manage mapping".

    ![Mapping Settings](/static/images/ddb-os-zetl7.jpg)
 1. In the "Backend roles" field, enter the Arn provided in the CloudFormation Stack Outputs. The attribute named "Role" provides the correct Arn.  
   Be absolutely sure you have removed any white space characters from the start and end of the ARN to ensure you do not have permissions issues later. Click "Map".  

    ![ Settings](/static/images/ddb-os-zetl8.jpg)
 1. Verify that the "all_access" Role now has a "Backend role" listed.

    ![ Settings](/static/images/ddb-os-zetl9.jpg)
