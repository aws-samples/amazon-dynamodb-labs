---
title: "Configure Environment"
menuTitle: "Configure Environment"
date: 2024-02-23T00:00:00-00:00
weight: 20
---
This chapter will create the environment on AWS as discussed in the Exercise Overview.
The CloudFormation template used below will create the DynamoDB Table and OpenSearch Domain as well as provide several Outputs to make organizing resource names easier.

1. Launch the CloudFormation template in US West 2 to deploy the resources in your account: [![CloudFormation](/static/images/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=us-west-2#/stacks/new?stackName=ddbzetl&templateURL=:param{key="lhol_ddb_os_zetl_setup_yaml"})  
    1. *Optionally, download [the YAML template](:param{key="lhol_ddb_os_zetl_setup_yaml"}) and launch it your own way*
 4. Click Next
 5. Confirm the Stack Name *ddbzetl* and update parameters if necessary (leave the default options if at all possible)
   ![Final Deployment Architecture](/static/images/ddb-os-zetl1.jpg)
 6. Click “Next” twice then check “I acknowledge that AWS CloudFormation might create IAM resources with custom names.”
 7. Click "Submit"
 8. The CloudFormation stack will take about 15 minutes to build the environment
  ![Final Deployment Architecture](/static/images/ddb-os-zetl2.jpg)