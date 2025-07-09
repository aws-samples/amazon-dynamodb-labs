---
title: "1. Getting Started"
menuTitle: "Getting Started"
date: 2024-02-23T00:00:00-00:00
weight: 10
chapter: true
description: "In this module, you configure your environment and download code that you will use throughout the lab."
---

## Background

Imagine you are building an online store. Most of your access patterns fit very well with DynamoDB's strengths. Looking up items by SKU, finding shopping cart contents, and viewing customer order history are all relatively straight forward key value queries.

As your application grows, though, you may want to add some additional access patterns. Search? Filtering? What about this whole "Generative AI" thing you've been hearing so much about. That might be an interesting differentiator for your app.

In this lab, we will learn how to integrate DynamoDB with Amazon OpenSearch Service to support those new access patterns.

## Getting Started

To set up this workshop, choose one of the following paths, depending on whether you are:

::alert[**If following the lab in your own AWS Account, you will create OpenSearch Service clusters, DynamoDB tables, and Secrets Manager resources that will incur a cost that could approach tens of dollars per day. Ensure you delete the CloudFormation stacks as soon as the lab is complete and verify all resources are deleted by checking the DynamoDB console, OpenSearch Service console, and Secrets Manager console. Make sure you [delete the Cloud9 environment](https://docs.aws.amazon.com/cloud9/latest/user-guide/delete-environment.html) as soon as the lab is complete**.]{type="warning"}

- :link[…running the workshop on your own (in your own AWS account)]{href="/dynamodb-opensearch-zetl/setup/on-your-own"}, which guides you to create resources using CloudFormation

- :link[…attending an AWS-hosted event (using AWS-provided access-code)]{href="/dynamodb-opensearch-zetl/setup/aws-ws-event"}


Once you have completed with either setup, continue on to:
- :link[Step 1: Setup AWS Cloud9 IDE]{href="/dynamodb-opensearch-zetl/setup/step1"}
