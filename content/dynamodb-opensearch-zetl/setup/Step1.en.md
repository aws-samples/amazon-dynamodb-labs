---
title: "Obtain & Review Code"
menuTitle: "Obtain & Review Code"
date: 2021-04-21T07:33:04-05:00
weight: 14
chapter: false
description: "To get started, you configure your environment and download code that you use during the lab."
---


Visual Studio Code (VS Code) is a lightweight, cross-platform source code editor designed for fast, modular software development. VS Code includes a code editor, debugger, and terminal. VS Code Server enables remote instances of VS Code to run on an EC2 instance, while the user interface runs locally in a browser.

Visual Studio Code Server is the environment where you will be executing the majority of this workshop. Your VS Code instance comes deployed with all the scripts and tools you'll need downloaded and pre-installed.

As a first step, you'll need to log into your VS Code instance and familiarize yourself with the user interface.

### To log in to your VS Code development environment:

1. Make sure you've logged into your workshop AWS account at least once. If you havn't opened it yet, do so now by clicking on the **Open AWS Console (us-west-2)** link located at the bottom left pane of this guide.
   
2. Click on the following link to navigate to your [CloudFormation Stacks](https://us-west-2.console.aws.amazon.com/cloudformation/home?region=us-west-2#/stacks), or browse to the CloudFormation Service on your own from the AWS Console. Next, click on the **dynamodb-opensearch-setup** stack.

![VS Code Environment](/static/images/cloudformation-stack.png)

3. Click on the **Outputs** tab. Find the output values for **VSCodeUrl** and **VSCodePassword**. Copy **VSCodePassword** to your clipboard, and then click on **VSCodeUrl**.

![CloudFormation Outputs](/static/images/cloudformation-outputs.png)

4. Paste your password into the **PASSWORD** field, then click **SUBMIT**.

![VS Code Login](/static/images/code-login.png)

You're now logged in to your VS Code environment. Take a moment to get familar with the user interface. You'll be using three main areas.

![VS Code Environment](/static/images/zetl-code-environment.png)

- **File explorer**: On the left side of the IDE, the file explorer shows a list of the files in your directory.
  
- **File editor**: On the upper right area of the IDE, the file editor is where you view and edit files that you’ve selected in the file explorer.
  
- **Terminal**: On the lower right area of the IDE, this is where you run commands to execute code samples.

You will see a directory in the VS Code file explorer named **LBED**. Click on the **>** to expand it.

The _LBED_ directory contains three things: 

- **product_en.json**: Example items that will be loaded into a DynamoDB table
- **credentials.sh**: Bash script that simplifies managing credentials when signing requests for OpenSearch
- **bedrock_query.py**: Python script that executes a query to Bedrock

Let's run the credentials script now to complete setup.

Run the following command in your VS Code terminal to set up your environment. This script exports multiple environmental variables containing your AWS credentials, IAM Role, and OpenSearch endpoint. These variables will allow you to run BASH and Python scripts throughout the workshop without needing to customize their contents to your speficic environment. Since we want the exports to be available in your current shell, make sure you include the "source" command ahead of the script. If you launch a new shell, you'll need to run the script again.(You can copy the commands using the Copy icon in the top right corner of the code block.)

```bash
cd LBED
source ./credentials.sh 
```

The script also has created a new file called **CloudFormation-Outputs.txt**. This file contains the same outputs you would see in the CloudFormation console. One less tab you need to keep open!

![VS Code CloudFormation Outputs](/static/images/code-cloudformation.png)

You are now ready to start the lab! In the next module, you will complete setup for each of the services used in this lab before moving on to integrate them.

You may now move on to the next step:

:link[Continue to Service Configuration]{href="/dynamodb-opensearch-zetl/service-config"}.  
