---
title: "2. Service Configuration"
menuTitle: "Service Configuration"
date: 2024-02-23T00:00:00-00:00
weight: 20
---
In this section, you will load data into your DynamoDB table and configure your OpenSearch Service resources.

Before beginning this section, make sure that :link[setup]{href="/dynamodb-opensearch-zetl/setup/"} has been completed for whichever way you're running this lab. Setup will deploy several resources.

Dependencies from Cloud9 CloudFormation Template:
  - S3 Bucket: Used to store the initial export of DynamoDB data for the Zero-ETL Pipeline.
  - IAM Role: Used to grant permissions for pipeline integration and queries.
  - Cloud9 IDE: Console for executing commands, building integrations, and running sample queries.

zETL CloudFormation Template Resources:
  - DynamoDB Table: DynamoDB table to store product descriptions. Has Point-in-time Recovery (PITR) and DynamoDB Streams enabled.
  - Amazon OpenSearch Service Domain: Single-node OpenSearch Service cluster to recieve data from DynamoDB and act as a vector database.

![Final Deployment Architecture](/static/images/migration-environment.png)