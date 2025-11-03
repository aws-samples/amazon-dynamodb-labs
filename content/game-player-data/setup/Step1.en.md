---
title: "Obtain & Review Code"
menuTitle: "Obtain & Review Code"
date: 2021-04-21T07:33:04-05:00
weight: 14
chapter: false
description: "To get started, you configure your environment and download code that you use during the lab."
---

During the first 60 seconds, the environment will automatically update extensions and plugins. Any startup notification can be safely dismissed. 
 
![VS Code Setup](/static/images/common/common-vs-code-01.png)

If a terminal is not available at the bottom left side of your screen, please open a new one like the following picture indicates.

![VS Code Setup](/static/images/common/common-vs-code-02.png)

Then run the command `aws sts get-caller-identity` just to verify that your AWS credentials have been properly configured.

![VS Code Setup](/static/images/common/common-vs-code-03.png)


In this lab, you use Python scripts to interact with the DynamoDB API. Run the following commands in your VS Code terminal to download and unpack this lab’s code.

```bash
cd ~/workshop/LGME
curl -sL https://amazon-dynamodb-labs.com/assets/battle-royale.zip -o battle-royal.zip && unzip -oq battle-royal.zip && rm battle-royal.zip
```

You should see two directories in the file explorer:

- **application**: The _application_ directory contains example code for reading and writing data in your table. This code is similar to code you would have in your real gaming application.

- **scripts**: The _scripts_ directory contains administrator-level scripts, such as for creating a table, adding a secondary index, or deleting a table.


You are now ready to start the lab. With DynamoDB, it is important to plan your data model up front so that you have fast, consistent performance in your application. In the next module, you will learn about planning your data model.
