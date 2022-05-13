+++
title = "Setup AWS Cloud9 IDE"
menuTitle = "Setup AWS Cloud9 IDE"
date = 2021-04-21T07:33:04-05:00
weight = 13
chapter = false
pre = ""
description = "To get started, you configure your environment and download code that you use during the lab."
+++


[AWS Cloud9](https://aws.amazon.com/cloud9/) is a cloud-based integrated development environment (IDE) that lets you write, run, and debug code with just a browser. AWS Cloud9 includes a code editor, debugger, and terminal. It also comes prepackaged with essential tools for popular programming languages and the AWS Command Line Interface (CLI) preinstalled so that you don’t have to install files or configure your laptop for this lab. Your AWS Cloud9 environment will have access to the same AWS resources as the user with which you signed in to the AWS Management Console.

### To set up your AWS Cloud9 development environment:

1. Choose **Services** at the top of the page, and then choose **Cloud9** under **Developer Tools**.
   
2. There would be an environment ready to use under **Your environments**.

3. Click on **Open IDE**, your IDE should open with a welcome note.

You should now see your AWS Cloud9 environment. You need to be familiar with the three areas of the AWS Cloud9 console shown in the following screenshot:

![Cloud9 Environment](/images/game-player-data/setup/cloud9-environment.png)

- **File explorer**: On the left side of the IDE, the file explorer shows a list of the files in your directory.
  
- **File editor**: On the upper right area of the IDE, the file editor is where you view and edit files that you’ve selected in the file explorer.
  
- **Terminal**: On the lower right area of the IDE, this is where you run commands to execute code samples.


The [AWS SDK for Python (Boto3)](https://aws.amazon.com/sdk-for-python/) enables you to use Python code to interact with AWS services like Amazon DynamoDB. In the AWS Cloud9 Terminal, confirm whether pip is already installed for the active version of Python by running this command:

```bash
python -m pip --version
```

Now, install the AWS SDK for Python (Boto3) by running: 

```bash
pip install boto3
```

Next, we would be downloading & reviewing the supporting code.