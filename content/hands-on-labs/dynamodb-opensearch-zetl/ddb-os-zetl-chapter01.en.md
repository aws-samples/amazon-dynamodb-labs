---
title: "Exercise Overview"
menuTitle: "Exercise Overview"
date: 2024-02-23T00:00:00-00:00
weight: 10
---
In this module, you will create DynamoDB and OpenSearch Service resources, configure integrations, and execute example queries.
All the initial resources required are deployed via [Amazon CloudFormation](https://aws.amazon.com/cloudformation/) template.
There is one CloudFormation template used in this exercise, but it has a dependency on the Cloud9 environment deployed in [Getting Started]({{< relref "/hands-on-labs/setup/setup.en.md" >}} "Getting Started"). The Cloudformation template will deploy following resources.

CloudFormation Template Resources:
  - DynamoDB Table: DynamoDB table to store product descriptions. Has Point-in-time Recovery (PITR) and DynamoDB Streams enabled.
  - Amazon OpenSearch Service Domain: Single-node OpenSearch Service cluster to recieve data from DynamoDB and act as a vector database.

Dependencies from Cloud9 CloudFormation Template:
  - S3 Bucket: Used to store the initial export of DynamoDB data for the Zero-ETL Pipeline.
  - IAM Role: Used to grant permissions for pipeline integration and queries.
  - Cloud9 IDE: Console for executing commands, building integrations, and running sample queries.


![Final Deployment Architecture](/static/images/migration-environment.png)