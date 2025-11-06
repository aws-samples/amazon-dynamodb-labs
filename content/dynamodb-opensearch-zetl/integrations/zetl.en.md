---
title: "Create the zero-ETL Pipeline"
menuTitle: "Create the zero-ETL Pipeline"
date: 2024-02-23T00:00:00-00:00
weight: 30
---
Amazon DynamoDB offers a zero-ETL integration with Amazon OpenSearch Service through the DynamoDB plugin for OpenSearch Ingestion. Amazon OpenSearch Ingestion offers a fully managed, no-code experience for ingesting data into Amazon OpenSearch Service. 

Please follow the steps to setup zero-ETL. Here we use the AWS Console instead of Curl commands:

 1. Open [OpenSearch Service](https://us-west-2.console.aws.amazon.com/aos/home?region=us-west-2#opensearch) within the Console

 2. Select **Pipelines** from the left pane and click on **"Create pipeline"**. 
![Create pipeline](/static/images/ddb-os-zetl13.jpg) 

 3. Select **"Blank"** from the Ingestion pipeline blueprints.
![BluePrint Selection](/static/images/CreatePipeline.png)

 4. Configure the source by selecting the source as **"Amazon DynamoDB"** and fill the details as below. Once done, click "Next"
![Configure source](/static/images/configure_source.png)

 5. Skip the **Processor** configuration

![Skip processor](/static/images/processor_blank.png) 

 6. Configure the sink by filling up the Opensearch details as below:
![Configure Sink](/static/images/configure_sink.png)

 7. Use the following content under **Schema mapping**:

```yaml
{
    "template": {
      "settings": {
        "index.knn": true,
        "default_pipeline": "product-en-nlp-ingest-pipeline"
      },
      "mappings": {
        "properties": {
          "ProductID": {
            "type": "keyword"
          },
          "ProductName": {
            "type": "text"
          },
          "Category": {
            "type": "text"
          },
          "Description": {
            "type": "text"
          },
          "Image": {
            "type": "text"
          },
          "combined_field": {
            "type": "text"
          },
          "product_embedding": {
            "type": "knn_vector",
            "dimension": 1536
          }
        }
      }
    }
}
```

Once done, click on **"Next"**

 8. Configure pipeline and then click "Next".

    ![Configure pipeline](/static/images/ddb-os-zetl14.jpg) 


 9. Click "Create pipeline".

    ![Create pipeline](/static/images/ddb-os-zetl15.jpg)

 10. **Wait until the pipeline has finished creating and status is "Active"**. This will take 5 minutes or more.


 After the pipeline is created, it will take some additional time for the initial export from DynamoDB and import into OpenSearch Service. After you have waited several more minutes, you can check if items have replicated into OpenSearch by making a query using the OpenSearch Dashboards feature called Dev Tools.
 
- To open Dev Tools, click on the menu in the top left of OpenSearch Dashboards, scroll down to the `Management` section, then click on `Dev Tools`. 
	
	![Devtools](/static/images/Devtools.png)

- Enter the following query in the left pane, then click the "play" arrow to execute it.

```text
GET /product-details-index-en/_search
```

- The output will the list of documents that have all the fields mentioned under the zero-ETL pipeline mapping.

 You may encounter a few types of results:
 - If you see a 404 error of type *index_not_found_exception*, then you need to wait until the pipeline is `Active`. Once it is, this exception will go away.
 - If your query does not have results, wait a few more minutes for the initial replication to finish and try again.

![Create pipeline](/static/images/ddb-os-zetl16.jpg)

Only continue once you see a return like the above, with a response body. Your hits may vary.