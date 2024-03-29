---
title: "Load DynamoDB Data"
menuTitle: "Load DynamoDB Data"
date: 2024-02-23T00:00:00-00:00
weight: 40
---
Next, you'll load example product data into your DynamoDB Table. Pipelines will move this data into OpenSearch Service in later steps.

## Open the Cloud9 IDE
If you have closed your Cloud9 IDE, follow these instructions to re-connect
 1. Open the "Outputs" tab of your recently deployed Stack in the CloudFormation Console.

    ![CloudFormation Outputs](/static/images/ddb-os-zetl2.jpg)
 1. Open the link for Cloud9IdeUrl in a new tab.


## Load Data

Load the sample data into your DynamoDB Table.
```bash
cd ~/environment/OpenSearchPipeline
aws dynamodb batch-write-item --request-items=file://product_en.json
```
 ![CloudFormation Outputs](/static/images/ddb-os-zetl11.jpg)