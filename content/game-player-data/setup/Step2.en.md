+++
title = "Obtain & Review Code"
menuTitle = "Obtain & Review Code"
date = 2021-04-21T07:33:04-05:00
weight = 14
chapter = false
pre = ""
description = "To get started, you configure your environment and download code that you use during the lab."
+++

In this lab, you use Python scripts to interact with the DynamoDB API. Run the following commands in your AWS Cloud9 terminal to download and unpack this lab’s code.

```bash
cd ~/environment
curl -sL https://s3.amazonaws.com/ddb-labs/battle-royale.tar | tar -xv
```

You should see two directories in the AWS Cloud9 file explorer:

- **application**: The _application_ directory contains example code for reading and writing data in your table. This code is similar to code you would have in your real gaming application.

- **scripts**: The _scripts_ directory contains administrator-level scripts, such as for creating a table, adding a secondary index, or deleting a table.


You are now ready to start the lab. With DynamoDB, it is important to plan your data model up front so that you have fast, consistent performance in your application. In the next module, you will learn about planning your data model.