---
title: "Obtain & Review Code"
menuTitle: "Obtain & Review Code"
date: 2021-04-21T07:33:04-05:00
weight: 14
chapter: false
description: "To get started, you configure your environment and download code that you use during the lab."
---


[AWS Cloud9](https://aws.amazon.com/cloud9/) is a cloud-based integrated development environment (IDE) that lets you write, run, and debug code with just a browser. AWS Cloud9 includes a code editor, debugger, and terminal. It also comes prepackaged with essential tools for popular programming languages and the AWS Command Line Interface (CLI) preinstalled so that you don’t have to install files or configure your laptop for this lab. Your AWS Cloud9 environment will have access to the same AWS resources as the user with which you signed in to the AWS Management Console.

### To set up your AWS Cloud9 development environment:

1. Choose **Services** at the top of the page, and then choose **Cloud9** under **Developer Tools**.
   
2. There would be an environment ready to use under **Your environments**.

3. Click on **Open IDE**, your IDE should open with a welcome note.

You should now see your AWS Cloud9 environment. You need to be familiar with the three areas of the AWS Cloud9 console shown in the following screenshot:

![Cloud9 Environment](/static/images/zetl-cloud9-environment.png)

- **File explorer**: On the left side of the IDE, the file explorer shows a list of the files in your directory.
  
- **File editor**: On the upper right area of the IDE, the file editor is where you view and edit files that you’ve selected in the file explorer.
  
- **Terminal**: On the lower right area of the IDE, this is where you run commands to execute code samples.



In this lab, you use Bash and Python scripts to interact with AWS services. Run the following commands in your AWS Cloud9 terminal to download and unpack this lab’s code.

```bash
cd ~/environment
curl -sL https://amazon-dynamodb-labs.com/assets/OpenSearchPipeline.zip -o OpenSearchPipeline.zip && unzip -oq OpenSearchPipeline.zip && rm OpenSearchPipeline.zip
```

You should see a directory in the AWS Cloud9 file explorer **OpenSearchPipeline**:

The _OpenSearchPipeline_ directory contains example items that will be loaded into a DynamoDB table, as Bash script to simplify managing credentials when signing requests for OpenSearch, and a python script for executing a query to Bedrock.

You are now ready to start the lab. In the next module, you will complete setup for each of the three services used in this lab before moving on to integrate them.

:link[Continue to Service Configuration]{href="/dynamodb-opensearch-zetl/service-config"}.  
