---
title: "Query and Conclusion"
menuTitle: "Query and Conclusion"
date: 2024-02-23T00:00:00-00:00
weight: 80
---
Now that you've created all required connectors and pipelines and data has replicated from DynamoDB into OpenSearch Service, you can make a query for a natural language product recommendation. This query will use OpenSearch as a vector database to find the product that most closely matches your desired intent.The contents of the OpenSearch index were created through the DynamoDB Zero ETL connector. When records are added to DynamoDB, the connector automatically moves them into OpenSearch. OpenSearch then uses the Titan Embeddings model to decorate that data. 

The script constructs a query that searches the OpenSearch index for products that are most relevant to your input text. This is done using a "neural" query, which leverages the embeddings stored in OpenSearch to find products with similar textual content. After retrieving relevant products, the script uses Bedrock to generate a more sophisticated response through the Claude model. This involves creating a prompt that combines your original query with the retrieved data and sending this prompt to Bedrock for processing. 

 1. Return to the Cloud9 IDE Console.
 1. In the console, execute the provided python script to make a query to Bedrock and return product results.
    ```bash
      python bedrock_query.py product_recommend en "I need a warm winter coat" $METADATA_AWS_REGION $OPENSEARCH_ENDPOINT $MODEL_ID 
    ```

    ![Query results](/static/images/ddb-os-zetl17.jpg)

Congratulations! You have completed the lab.
