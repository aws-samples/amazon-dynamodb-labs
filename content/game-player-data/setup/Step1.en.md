---
title: "Obtain & Review Code"
menuTitle: "Obtain & Review Code"
date: 2021-04-21T07:33:04-05:00
weight: 14
chapter: false
pre: ""
description: "To get started, you configure your environment and download code that you use during the lab."
---


[AWS Cloud9](https://aws.amazon.com/cloud9/) is a cloud-based integrated development environment (IDE) that lets you write, run, and debug code with just a browser. AWS Cloud9 includes a code editor, debugger, and terminal. It also comes prepackaged with essential tools for popular programming languages and the AWS Command Line Interface (CLI) preinstalled so that you don’t have to install files or configure your laptop for this lab. Your AWS Cloud9 environment will have access to the same AWS resources as the user with which you signed in to the AWS Management Console.

### To set up your AWS Cloud9 development environment:

1. Choose **Services** at the top of the page, and then choose **Cloud9** under **Developer Tools**.
   
2. There would be an environment ready to use under **Your environments**.

3. Click on **Open IDE**, your IDE should open with a welcome note.

You should now see your AWS Cloud9 environment. You need to be familiar with the three areas of the AWS Cloud9 console shown in the following screenshot:

![Cloud9 Environment](/static/images/game-player-data/setup/cloud9-environment.png)

- **File explorer**: On the left side of the IDE, the file explorer shows a list of the files in your directory.
  
- **File editor**: On the upper right area of the IDE, the file editor is where you view and edit files that you’ve selected in the file explorer.
  
- **Terminal**: On the lower right area of the IDE, this is where you run commands to execute code samples.



In this lab, you use Python scripts to interact with the DynamoDB API. Run the following commands in your AWS Cloud9 terminal to download and unpack this lab’s code.

```bash
cd ~/environment
curl -sL https://amazon-dynamodb-labs.com/static/game-player-data/battle-royale.tar | tar -xv
```

You should see two directories in the AWS Cloud9 file explorer:

- **application**: The _application_ directory contains example code for reading and writing data in your table. This code is similar to code you would have in your real gaming application.

- **scripts**: The _scripts_ directory contains administrator-level scripts, such as for creating a table, adding a secondary index, or deleting a table.


You are now ready to start the lab. With DynamoDB, it is important to plan your data model up front so that you have fast, consistent performance in your application. In the next module, you will learn about planning your data model.
