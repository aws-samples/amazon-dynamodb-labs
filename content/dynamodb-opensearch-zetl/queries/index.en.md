---
title: "4. Query and Conclusion"
menuTitle: "Query and Conclusion"
date: 2024-02-23T00:00:00-00:00
weight: 40
---
At this point you've setup all the required connectors and pipelines and data has replicated from DynamoDB into OpenSearch Service, so it's time to reap the rewards and query your data in various ways based on the use-case. 
- Do key/value lookup directly to DynamoDB
- Execute search queries against OpenSearch
- Use Bedrock together with OpenSearch for natural language product recommendation. 

Please follow the steps to test the query system: 

 1. Return to the VS Code IDE Console.

 1. First, let's make a request to DynamoDB directly

    ```bash
      aws dynamodb get-item \
          --table-name ProductDetails \
          --key '{"ProductID": {"S": "S020"}}'
    ```

    This is an example of a key/value lookup where DynamoDB excels. It returns product details for a specific product, identified by its ProductID.

 1. Next, let's make a search query to OpenSearch. Ask for skirts that include "Spandex" in their description. Here, we are **not performing neural search** but text search against OpenSearch.

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

    Try changing `Spandex` to `Polyester` and see how the results change. 

 1. Finally, let's ask Bedrock to provide some product recommendations using one of the scripted provided with the lab. 


    This query will use OpenSearch as a vector database to find the product that most closely matches your desired intent. The contents of the OpenSearch index were created through the DynamoDB Zero-ETL connector. When records are added to DynamoDB, the connector automatically moved them into OpenSearch. OpenSearch then uses the Titan Embeddings model to decorate that data. 

    The script constructs a query that searches the OpenSearch index for products that are most relevant to your input text. This is done using a **"neural" query**, which leverages the **embeddings stored in OpenSearch** to find products with similar textual content. After retrieving relevant products, the script uses **Bedrock** to generate a more sophisticated response through the **Claude model**. This involves creating a prompt that combines your original query with the retrieved data and sending this prompt to Bedrock for processing. This is called **Retrieval augmented generation (RAG)** and combines LLMs with external knowledge bases to improve their outputs. Here, we are using OpenSearch as our knowledge base to provide the relevant context to the LLM to generate accurate response.

    - If you open the **"bedrock_query.py"** and check the query, you will find below snippet:
    ```bash
    query = {
      "size": 5,
      "sort": [
        {
          "_score": {
            "order": "desc"
          }
        }
      ],
      "_source": {
        "includes": ["ProductName", "Category", "Description", "ProductID","Image"]
      },
      "query": {
        "neural": {
          "product_embedding": {
            "query_text": input_text,
            "model_id": model_id,
            "k": 10
          }
        }
      }
    }
    ```

    - This is a **neural based retrieval to find the most relevant documents with the help of product_embedding (contains Vector embeddings). It also provides the model_id and "k" to indicate the number of results to return**.
    
    
    Let's execute the script. Go to VS Code and execute the Python script like so. The result will have the LLM response and the OpenSearch-retrieved data as well. 

    ```bash
    python bedrock_query.py product_recommend en "I need a warm winter coat" $METADATA_AWS_REGION $OPENSEARCH_ENDPOINT $MODEL_ID | jq .
    ```

    ![Query results](/static/images/ddb-os-zetl17.jpg)

 1. Try adding a new item to your DynamoDB table, some wool socks.

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

 1. Try modifying the DynamoDB get-item above to retrieve your new item. It should appear. Then try modifying the OpenSearch query to search for "Socks" that contain "Wool". Finally, tell Bedrock "I need warm socks for hiking in winter". Did it recommend your new item?

::alert[Don't just stop there with your queries. Trying asking for clothing for winter (will it recommend products with wool?) or for bedtime. Note that there is a very small catalog of products to be embedded, so your search terms should be limited based on what you saw when you reviewed the DynamoDB table.]{header="Keeping querying!" type="info"}

Congratulations! You have completed the workshop.

::alert[_If running in you own account, remember to delete the CloudFormation Stack after completing the lab to avoid unexpected charges._]{type="warning"}