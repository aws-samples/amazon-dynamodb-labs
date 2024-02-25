---
title: "Load DynamoDB Data"
menuTitle: "Load DynamoDB Data"
date: 2024-02-23T00:00:00-00:00
weight: 50
---
Next, you'll load example product data into your DynamoDB Table. Pipelines will move this data into OpenSearch Service in later steps.

 1. Open the "Outputs" tab of your recently deployed Stack in the CloudFormation Console.
   ![CloudFormation Outputs](/static/images/ddb-os-zetl2.jpg)
 2. Open the link for Cloud9IdeUrl in a new tab.
 3. Download the zip containing the zip containing sample data and scripts.
    ```bash
      wget https://s3.amazonaws.com/amazon-dynamodb-labs.com/assets/OpenSearchPipeline.yaml
    ```
 4. Unzip the contents of the zip file.
    ```bash
      unzip OpenSearchPipeline.zip 
    ```
 5. Change into the directory.
    ```bash
      cd OpenSearchPipeline
    ```
 6. Load the sample data into your DynamoDB Table.
    ```bash
      aws dynamodb batch-write-item --request-items=file://product_en.json
    ```