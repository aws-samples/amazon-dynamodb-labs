---
title: "Stage 4: DynamoDB Integration"
date: 2025-09-02T15:41:04-05:00
weight: 30
chapter: true
---
::alert[In this workshop this stage has already been completed for you. Please review the artifacts available on `/artifacts/stage-04` ]{type="info"}

## Setting Up DynamoDB Infrastructure

Stage 4 is where you actually implement the DynamoDB side of your dual database system. Think of this as installing the wiring and connections for your second database engine - you're building all the infrastructure needed to make DynamoDB work with your application.

This stage focuses on creating the actual DynamoDB tables, setting up the AWS SDK connections, and implementing the data transformation logic that converts your MySQL data into DynamoDB format.

## What You'll Build

Using your migration contract as the blueprint, you'll create the actual DynamoDB tables with the exact specifications from your data model:

- **Users Table**: With partition key (PK) and sort key (SK), plus the three GSIs (GSI1, GSI2, GSI3) you designed
- **Products Table**: With its partition/sort keys and two GSIs (GSI1, GSI2)  
- **Orders Table**: With its keys and single GSI (GSI1)

Each table needs to be configured with the right capacity settings, security policies, and monitoring to handle your application's traffic.

You'll set up the connection between your application and DynamoDB using the AWS SDK, Setting up the DynamoDB client with proper authentication, you will connect to the proper AWS regions and make sure you configure the right information in the SDK settings for retries.

At this stage you will implement the transformation logic that converts MySQL data into DynamoDB items, you will need to re-write your APIs to work with DynamoDB SDK instead of SQL, you will need to handle the difference between data types and how to flatten the relational joins into single DynamoDB items. This step requires a lot of testing and validation to make sure you don't loose any data and you always provide the same API response regardless of the method, if you retrieve the elements from the Shopping cart, you should return the list of them regardless of the Database who has them. 

## Test driven development

All the refactoring stages, use Test Driven Development, this ensures backward compatibility and avoid changing working/existing logic. You will first create a non-working unit test, and iteratively modify the code until the unit test passes. To ensure full compatibility we provide instructions to the LLMs to re-run the Unit, Integration and End-to-end testing, every time a new functionality is added. (This is why it takes so long to complete!)

## Next Steps

By building robust DynamoDB infrastructure in Stage 4, you create a reliable foundation for the migration control system you'll build in Stage 5. If the DynamoDB implementation is shaky, the entire migration process becomes risky.  The transformation engine you build here ensures that data moving from MySQL to DynamoDB maintains its accuracy and completeness. This is critical for maintaining user trust during the migration.

This stage transforms your migration contract from a paper plan into working code that can actually store and retrieve data from DynamoDB. Once Stage 4 is complete, you have a fully functional NoSQL backend ready to be integrated into your migration workflow.
