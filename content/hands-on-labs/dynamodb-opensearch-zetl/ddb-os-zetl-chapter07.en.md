---
title: "Create zero-ETL Pipeline"
menuTitle: "Create zero-ETL Pipeline"
date: 2024-02-23T00:00:00-00:00
weight: 70
---
Amazon DynamoDB offers a zero-ETL integration with Amazon OpenSearch Service through the DynamoDB plugin for OpenSearch Ingestion. Amazon OpenSearch Ingestion offers a fully managed, no-code experience for ingesting data into Amazon OpenSearch Service. 

 1. Open [OpenSearch Service Ingestion Pipelines](https://us-west-2.console.aws.amazon.com/aos/home?region=us-west-2#opensearch/ingestion-pipelines)
 1. Click "Create pipeline"

    ![Create pipeline](/static/images/ddb-os-zetl13.jpg)

 1. Name your pipeline, and include the following for your pipeline configuration. The configuration contains multiple values that need to be updated. The needed values are provided in the CloudFormation Stack Outputs as "Region", "Role", "S3Bucket", "DdbTableArn", and "OSDomainEndpoint".
    ```yaml
      version: "2"
      dynamodb-pipeline:
        source:
          dynamodb:
            acknowledgments: true
            tables:
              # REQUIRED: Supply the DynamoDB table ARN
              - table_arn: "{DDB_TABLE_ARN}"
                stream:
                  start_position: "LATEST"
                export:
                  # REQUIRED: Specify the name of an existing S3 bucket for DynamoDB to write export data files to
                  s3_bucket: "{S3BUCKET}"
                  # REQUIRED: Specify the region of the S3 bucket
                  s3_region: "{REGION}"
                  # Optionally set the name of a prefix that DynamoDB export data files are written to in the bucket.
                  s3_prefix: "pipeline"
            aws:
              # REQUIRED: Provide the role to assume that has the necessary permissions to DynamoDB, OpenSearch, and S3.
              sts_role_arn: "{ROLE}"
              # REQUIRED: Provide the region
              region: "{REGION}"
        sink:
          - opensearch:
              hosts:
                  # REQUIRED: Provide an AWS OpenSearch endpoint, including https://
                [
                  "{OS_DOMAIN_ENDPOINT}"
                ]
              index: "product-details-index-en"
              index_type: custom
              template_type: "index-template"
              template_content: |
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
                          "dimension": 1536,
                          "method": {
                            "engine": "nmslib",
                            "name": "hnsw",
                            "space_type": "l2"
                          }
                        }
                      }
                    }
                  }
                }
              aws:
                # REQUIRED: Provide the role to assume that has the necessary permissions to DynamoDB, OpenSearch, and S3.
                sts_role_arn: "{ROLE}"
                # REQUIRED: Provide the region
                region: "{REGION}"
    ```
 1. Under Network, select "Public access", then click "Next".

    ![Create pipeline](/static/images/ddb-os-zetl14.jpg)

 1. Click "Create pipeline".

    ![Create pipeline](/static/images/ddb-os-zetl15.jpg)

 1. Wait until the pipeline has finished creating. After the pipeline is created, it will take some additional time for the initial export from DynamoDB and import into OpenSearch Service. After you have waited several minutes, you can check if items have replicated into OpenSearch by making a query in Dev Tools in the OpenSearch Dashboards. If your query does not have results, wait a few more minutes for the initial replication to finish.
 
    ![Create pipeline](/static/images/ddb-os-zetl16.jpg)
