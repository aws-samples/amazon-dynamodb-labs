---
title: "2.5 Data model redesign"
menuTitle: "Data model redesign"
date: 2025-09-02T16:43:04-05:00
weight: 36
chapter: false
---

::alert[Some of the workshop executions the validations presented in this section has been done table by table. Given the undeterministic nature of LLMs we can't assume the output from every workshop participant will be the same. Please make sure before you continue with task 4, that your data model is writen as intended and you have validated all the recommendations in this section.]{type="warning"}

## Initiating the Design Refinement Process

At this stage, you'll execute the most critical phase of the data modeling process: iterative design refinement. This process transforms your initial conceptual model into a DynamoDB schema that efficiently supports all identified access patterns.

This task involves comprehensive analysis and redesign of your initial data model based on the validation results from the previous step. The DynamoDB MCP Server will perform detailed optimization analysis, potentially recommending significant structural changes to improve performance and cost efficiency.

## Critical Review and Validation Phase

Once the redesign is complete, thoroughly examine the updated `dynamodb_data_model.md` file. Compare the new design against all previously identified requirements, access patterns, and performance criteria. This review process mirrors real-world database design workflows where architects spend considerable time validating and iterating on designs before implementation.

The design refinement process often reveals opportunities for optimization that weren't apparent in the initial modeling phase. Pay particular attention to:

- **Entity consolidation opportunities** where related data can be co-located for improved query performance
- **GSI optimization** to minimize the number of secondary indexes while maintaining query flexibility  
- **Partition key distribution** to ensure even data distribution and avoid hot partition issues
- **Sort key design** that enables efficient range queries and supports multiple access patterns

This iterative approach reflects industry best practices where database designs undergo multiple refinement cycles before reaching production readiness.

## Design Validation Checkpoints

As the system progresses through task 3.3, verify that the final design adheres to established naming conventions and structural standards. Specifically, ensure no entity prefixes are applied to primary key values such as `PROD_<product_id>` or `USER_<user_id>` or `USER_<email>`.

The validation process serves as quality assurance, catching potential issues before they propagate to subsequent implementation phases. Investing time in thorough validation at this stage prevents costly rework during later development phases as the quality of each stage's output depends on the quality of it's input.

## Final Schema Verification

Confirm that the final data model maintains the standardized naming convention for tables and indexes:

- **Table 1**: Users Table with three Global Secondary Indexes named GSI1, GSI2, GSI3
- **Table 2**: Products Table with two Global Secondary Indexes named GSI1, GSI2  
- **Table 3**: Orders Table with one Global Secondary Index named GSI1

This generic naming convention provides flexibility for future schema evolution while maintaining consistency across the application architecture.

The standardized naming approach also simplifies application code by providing predictable patterns for GSI references, reducing the likelihood of configuration errors during deployment.

When you are happy with all the review process you can continue with the next step. 

:image[3 Table Design]{src="/static/images/modernizer/2/LGAM-02-stage02-16.png" disableZoom=false width=850}
