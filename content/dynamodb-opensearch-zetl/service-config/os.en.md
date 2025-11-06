---
title: "Configure OpenSearch Service Permissions"
menuTitle: "Configure OpenSearch Service Permissions"
date: 2024-02-23T00:00:00-00:00
weight: 20
---
The OpenSearch Service Domain deployed by the CloudFormation Template uses Fine-grained access control (FGAC). In order to configure easy integrations between OpenSearch Service, DynamoDB, and Bedrock, we need to map the IAM role that was created by the CloudFormation Template and will be used by the integration into an OpenSearch Service role called "all_access". With that, the IAM role will have permissions to access OpenSearch.

For this section, we will need to know the names and paths of various resources constructed by the CloudFormation Template. For example, the URL to the OpenSearch Dashboards, the access credentials, and other values. These can be found in the Outputs of the **CloudFormation-Outputs.txt** file created by the credentials.sh script you ran in the previous section. Open this file so that the values are easily available.

In a production environment as a best practice, you should configure roles with the least privilege required for exactly what's needed by your application. For simplicity in this lab, we will use the "all_access" OpenSearch Service role.

 1. In the **CloudFormation-Outputs.txt** file, find the value for **OpenSearchPassword** and copy it to your clipboard. Next, find the value for **OSDashboardsURL** and hold ctrl while you click it to follow the link.

    ![OpenSearch Dashboard Login](/static/images/code-cloudformation-opensearch.png)
 1. Type "master-user" as the username, paste the password from your clipboard, then click **Log in**.

    ![OpenSearch Service Dashboards](/static/images/ddb-os-zetl4-small.jpg)
 1. You will get the 'Welcome to OpenSearch Dashboards'. Select **Explore on my own**.

    ![Welcome Page OpenSearch](/static/images/Welcome-os.png)
 1. When prompted to select your tenant, choose *Global* and click **Confirm**. Dismiss any pop ups.

    ![OpenSearch Service Dashboards](/static/images/ddb-os-zetl18-small.jpg)
 1. Open the top left menu and select **Security** under the *Management* section.

    ![Security Settings](/static/images/ddb-os-zetl5-small.jpg) 
 1. Open the "Roles" tab, search for "all_access" and then click on the "all_access" role.

    ![Roles Settings](/static/images/ddb-os-zetl6-small.jpg) 
 1. Open the "Mapped users" tab, then select "Manage mapping".

    ![Mapping Settings](/static/images/ddb-os-zetl7-small.jpg)
 1. In the "Backend roles" field, enter the ARN provided in the **CloudFormation-Outputs.txt** file. The attribute named "Role" provides the correct ARN.  
   Be absolutely sure you have removed any white space characters from the start and end of the ARN to ensure you do not have permissions issues later. Click "Map".  

    ![ Settings](/static/images/ddb-os-zetl8-small.jpg)
 1. Verify that the "all_access" Role now has a "Backend role" listed.

    ![ Settings](/static/images/ddb-os-zetl9-small.jpg)
