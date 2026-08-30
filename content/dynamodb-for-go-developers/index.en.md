---
title: "LGOD: DynamoDB for Go Developers"
chapter: true
description: "200 level: Hands-on with DynamoDB APIs, single table design, and indexes using Go."
weight: 25
---

In this workshop, you learn how to use [Amazon DynamoDB](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html) with the AWS SDK for Go v2. You start from a ready-to-run project (the workshop's **lab branch**) and complete a complete inventory management system by filling in each DynamoDB API operation, guided step by step. Worked examples show you the pattern; you implement the rest.

Here's what this workshop includes:

::children{depth=1}

### Target audience

This workshop is designed for Go developers who want to learn DynamoDB by building a real application. You clone the lab-branch project, provision the table with CloudFormation, then fill in the Go code that reads and writes data, queries with indexes, and performs transactions - running each operation directly from `go run .` as you complete it.

### Requirements

#### Go programming experience
- Familiarity with Go structs, interfaces, and error handling
- Basic understanding of Go modules (`go mod`)
- Comfort with the command line

#### Basic knowledge of AWS services
- An AWS account with permissions to create DynamoDB tables
- AWS CLI installed and configured with credentials
- Among other services this lab will guide you through the use of [Amazon DynamoDB](https://aws.amazon.com/dynamodb/)

#### Basic understanding of DynamoDB
- If you're not familiar with DynamoDB, consider reviewing the documentation on "[What is Amazon DynamoDB?](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html)"

### What you'll build

A complete inventory management system featuring:
- **Users** with profiles and multiple addresses
- **Orders** with status tracking and lifecycle management
- **Order Items** with pricing and quantities
- **Single table design** with multiple access patterns

### What you'll learn

- Provisioning DynamoDB tables and indexes with CloudFormation (control plane vs. data plane)
- Writing items with `PutItem` and `BatchWriteItem`
- Reading items with `GetItem` and `Query`
- Querying Global Secondary Indexes (GSI) for cross-partition lookups
- Querying Local Secondary Indexes (LSI) for alternate sort orders
- Using multi-attribute key GSIs as a modern alternative to concatenated keys
- Updating items with expressions and conditions
- Deleting items with safeguards
- Atomic operations with `TransactWriteItems` and `TransactGetItems`
- Scanning tables with pagination and parallel segments
