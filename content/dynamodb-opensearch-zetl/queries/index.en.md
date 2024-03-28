---
title: "4. Query and Conclusion"
menuTitle: "Query and Conclusion"
date: 2024-02-23T00:00:00-00:00
weight: 40
---
Now that you've created all required connectors and pipelines and data has replicated from DynamoDB into OpenSearch Service, you have quite a few options for how you want to query your data. You can do key/value looksups directly to DynamoDB, execute search queries against OpenSearch, and use Bedrock togther with Opensearch for natural language product recommendation. 

This query will use OpenSearch as a vector database to find the product that most closely matches your desired intent.The contents of the OpenSearch index were created through the DynamoDB Zero ETL connector. When records are added to DynamoDB, the connector automatically moves them into OpenSearch. OpenSearch then uses the Titan Embeddings model to decorate that data. 

The script constructs a query that searches the OpenSearch index for products that are most relevant to your input text. This is done using a "neural" query, which leverages the embeddings stored in OpenSearch to find products with similar textual content. After retrieving relevant products, the script uses Bedrock to generate a more sophisticated response through the Claude model. This involves creating a prompt that combines your original query with the retrieved data and sending this prompt to Bedrock for processing. 

 1. Return to the Cloud9 IDE Console.

 1. First, let's make a request to DynamoDB directly

    ```bash
      aws dynamodb get-item \
          --table-name ProductDetails \
          --key '{"ProductID": {"S": "S020"}}'
    ```

    This is an example of a key/value lookup that DynamoDB excels at. It returns product details for a specific product, identified by its ProductID.

 1. Next, let's make a search query to OpenSearch. We'll find skirts that include "Spandex" in their description.

    ```bash
    curl --request POST \
      ${OPENSEARCH_ENDPOINT}/product-details-index-en/_search \
      --header 'Content-Type: application/json' \
      --header 'Accept: application/json' \
      --header "x-amz-security-token: ${METADATA_AWS_SESSION_TOKEN}" \
      --aws-sigv4 aws:amz:${METADATA_AWS_REGION}:es \
      --user "${METADATA_AWS_ACCESS_KEY_ID}:${METADATA_AWS_SECRET_ACCESS_KEY}" \
      --data-raw '{
        "_source": {
          "excludes": ["product_embedding"]
        },
        "query": {
          "bool": {
            "must": [
              {
                "match": {
                  "Category": "Skirt"
                }
              },
              {
                "match_phrase": {
                  "Description": "Spandex"
                }
              }
            ]
          }
        }
      }' | jq .
    ```

    Try changing "Spandex" to "Polyester" and see how the results change.

 1. Finally, let's ask Bedrock to provide some product recommendations using one of the scripted provided with the lab. 

    This query will use OpenSearch as a vector database to find the product that most closely matches your desired intent.The contents of the OpenSearch index were created through the DynamoDB Zero ETL connector. When records are added to DynamoDB, the connector automatically moves them into OpenSearch. OpenSearch then uses the Titan Embeddings model to decorate that data. 

    The script constructs a query that searches the OpenSearch index for products that are most relevant to your input text. This is done using a "neural" query, which leverages the embeddings stored in OpenSearch to find products with similar textual content. After retrieving relevant products, the script uses Bedrock to generate a more sophisticated response through the Claude model. This involves creating a prompt that combines your original query with the retrieved data and sending this prompt to Bedrock for processing. 


    In the console, execute the provided python script to make a query to Bedrock and return product results.
    ```bash
      python bedrock_query.py product_recommend en "I need a warm winter coat" $METADATA_AWS_REGION $OPENSEARCH_ENDPOINT $MODEL_ID 
    ```

    ![Query results](/static/images/ddb-os-zetl17.jpg)

 1. Try adding a new item to your DynamoDB table.

    ```bash
    aws dynamodb put-item \
        --table-name ProductDetails \
        --item '{
            "ProductID": {"S": "S021"},
            "Category": {"S": "Socks"},
            "Description": {"S": "{\"Style\": \"Outdoor\", \"Pattern\": \"Striped\", \"Length\": \"Knee-High\", \"Type\": \"Thick\", \"Fabric\": \"Wool\", \"Composition\": \"80% Wool, 20% Nylon\", \"Care Instructions\": \"Hand wash cold, lay flat to dry\", \"Ideal For\": \"Outdoor Activities\", \"Stretch\": \"Moderate\", \"Opacity\": \"Opaque\", \"Lining\": \"No\", \"Pockets\": \"No Pockets\", \"Closure\": \"Pull Up\", \"Shoe Height\": \"Knee-High\", \"Occasion\": \"Outdoor\", \"Season\": \"Fall, Winter\"}"},
            "Image": {"S": "https://example.com/S021.jpg"},
            "ProductName": {"S": "Striped Wool Knee-High Socks"}
        }'
    ```

 1. Try modifying the DynamoDB get-item above to retrieve your new item. Next, try modifying the OpenSearch query to search for "Socks" that contain "Wool". Finally, tell Bedrock "I need warm socks for hiking in winter". Did it recommend your new item?

Congratulations! You have completed the lab.

::alert[_If running in you own account, remember to delete the CloudFormation Stack after completing the lab to avoid unexpected charges._]