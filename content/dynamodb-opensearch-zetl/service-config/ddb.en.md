---
title: "Load DynamoDB Data"
menuTitle: "Load DynamoDB Data"
date: 2024-02-23T00:00:00-00:00
weight: 40
---
Next, you'll load example product data into your DynamoDB Table. In later step, we'll setup a pipeline to move this data into OpenSearch Service.

## Load and Review Data
Return to the VS Code IDE. If you accidentally closed the IDE, you may find the URL in the `Outputs` section of the CloudFormation stack.

Load the sample data into your DynamoDB Table. You can look at the JSON file if you want to see the small number of item being loaded.

```bash
cd ~/workshop/LBED
aws dynamodb batch-write-item --request-items=file://product_en.json
```
 ![CloudFormation Outputs](/static/images/ddb-os-zetl11.png)

::alert[_You should see an empty **UnprocessedItems** list. If it is not, it means some of the operations might have failed which needs to be investigated._]


 Next, navigate to the [DynamoDB section of the AWS Management Console](https://us-west-2.console.aws.amazon.com/dynamodbv2/home?region=us-west-2#dashboard). Click `Explore items` on the left panel and then select the `ProductDetails` table. You can review the product names to get an idea for what kind of natural language searches you might want to test with at the end of the lab.

  ![DynamoDB Console](/static/images/ddb-os-zetl19-small.jpg)