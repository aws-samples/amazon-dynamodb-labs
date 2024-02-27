---
title: "Query and Conclusion"
menuTitle: "Query and Conclusion"
date: 2024-02-23T00:00:00-00:00
weight: 80
---
Now that you've created all required connectors and pipelines and data has replicated from DynamoDB into OpenSearch Service, you can make a Bedrock query for a natural language product recommendation. This query will use OpenSearch as a vector database to find the product that most closely matches your desired intent.

 1. Return to the Cloud9 IDE Console.
 1. In the console, execute the provided python script to make a query to Bedrock and return product results.
    ```bash
      python bedrock_query.py product_recommend en "I need a warm winter coat" $METADATA_AWS_REGION $OPENSEARCH_ENDPOINT $MODEL_ID 
    ```
    ![Query results](/static/images/ddb-os-zetl7.jpg)

Congratulations! You have completed the lab.
