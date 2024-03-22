---
title: "Enable Amazon Bedrock Models"
menuTitle: "Enable Amazon Bedrock Models"
date: 2024-02-23T00:00:00-00:00
weight: 40
---
Amazon Bedrock is a fully managed service that offers a choice of high-performing foundation models (FMs) from leading AI companies like AI21 Labs, Anthropic, Cohere, Meta, Mistral AI, Stability AI, and Amazon via a single API, along with a broad set of capabilities you need to build generative AI applications with security, privacy, and responsible AI.

In this application, Bedrock will be used to make natural language product recommendation queries using OpenSearch Service as a vector database.

Bedrock requires different FMs to be enabled before they are used.

 1. Open [Amazon Bedrock Model Access](https://us-west-2.console.aws.amazon.com/bedrock/home?region=us-west-2#/modelaccess)
 1. Click on "Manage model access"

    ![Manage model access](/static/images/ddb-os-zetl10.jpg)
 1. Select "Titan Embeddings G1 - Text" and "Claude", then click "Save changes"

    ![Manage model access](/static/images/ddb-os-zetl11.jpg)
1. Wait until you are granted access to both models before continuing. The *Access status* should say *Access granted* before moving on.  
::alert[_Do not continue unless the base models "Claude" and "Titan Embeddings G1 - Text" are granted to your account._]
