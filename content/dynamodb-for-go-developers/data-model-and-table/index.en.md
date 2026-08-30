---
title: "2. Data Model and Table"
date: 2021-04-21T07:33:04-05:00
weight: 20
chapter: true
description: "Design the single table data model and provision the table with CloudFormation."
---

In this chapter, you learn the single table design pattern and then provision the DynamoDB table with all its indexes using CloudFormation. By the end of this module, you have a working table ready to accept data.

Provisioning the table with infrastructure-as-code - rather than from application code - mirrors how you manage DynamoDB in production. You will see this distinction (control plane vs. data plane) throughout the module.

::children{depth=1}
