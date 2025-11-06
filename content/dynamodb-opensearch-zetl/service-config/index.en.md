---
title: "2. Service Configuration"
menuTitle: "Service Configuration"
date: 2024-02-23T00:00:00-00:00
weight: 20
---

At this point, some configuration has already been done by the CloudFormation Template that prepared the environment. 

  - **DynamoDB Table**: We have a DynamoDB table intended to store product descriptions. It has Point-in-time Recovery (PITR) and DynamoDB Streams enabled.
  - **Amazon OpenSearch Service Domain**: We have a single-node OpenSearch Service cluster built. It will recieve data from DynamoDB and act as a vector database.

![Final Deployment Architecture](/static/images/serviceconf.png)

We also have a few supporting resources that were created from the CloudFormation Template:

  - **Visual Studio Code Server IDE**: Console for executing commands, building integrations, and running sample queries.
  - **S3 Bucket**: Used to store the initial export of DynamoDB data for the Zero-ETL Pipeline.
  - **IAM Role**: Used to grant permissions for pipeline integration and queries.

We have a few tasks to perform still. We must load data into DynamoDB and configure OpenSearch permissions before we can begin building the required pipelines. We will start by configuring OpenSearch.