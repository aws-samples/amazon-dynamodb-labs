---
title: "LBED: Enable Gen AI and search in Amazon DynamoDB workloads with Amazon Bedrock and the zero-ETL connector to Amazon OpenSearch Service"
date: 2024-02-23T00:00:00-00:00
weight: 20
chapter: true
description: "In this module you will have a hands on experience setting up DynamoDB zero-ETL integration with Amazon OpenSearch Service."
---

In this module you will have a hands on experience setting up DynamoDB zero-ETL integration with Amazon OpenSearch Service. You will create a pipeline from a DynamoDB table to OpenSearch Service, create an Amazon Bedrock Connector in OpenSearch Service, and query Bedrock leveraging OpenSearch Service as a vector store.
At the end of this lesson, you should feel confident in your ability to integrate DynamoDB with OpenSearch Service to support context aware reasoning applications.

Pairing Amazon DynamoDB with Amazon OpenSearch Service is a common architecture pattern for applications that need to combine the high scalability and performance of DynamoDB for transactional workloads with the powerful search and analytics capabilities of OpenSearch.

DynamoDB is a NoSQL database designed for high availability, performance, and scalability and focused on key/value operations. OpenSearch Service provides advanced search features such as full-text search, faceted search, and complex querying capabilities. Combined, these two services can satisfy a wide variety of application use cases.

This module will allow you to set up one such use case. DynamoDB will be the source of truth for product catalog information and OpenSearch will provide vector search capabilities to enable Amazon Bedrock (a generative AI service) to make product recommendations.

::alert[_This lab creates OpenSearch Service, DynamoDB, Amazon Bedrock, and Secrets Manager resources. If running in you own account, these resources will incur charges of approximately $30 a month. Remember to delete the CloudFormation Stack after completing the lab._]

![Final Deployment Architecture](/static/images/ddb-os-zetl.png)