---
title: "Stage 2: Data modeling"
date: 2025-09-02T15:41:04-05:00
weight: 30
chapter: true
---

## DynamoDB Data Modeling Workshop

Having completed the application analysis in Stage 1, you now understand the existing MySQL schema, identified access patterns, and established performance requirements. Stage 2 focuses on translating this relational data model into an optimized DynamoDB design that supports all identified access patterns while leveraging the advantages of NoSQL.

This stage requires active collaboration between you as a human architect and and AI tools assisting with technical implementation. You'll guide the design process while the AI makes recommendations for DynamoDB data modeling practices.

## Interactive Design Process

The task list for this stage begins empty by design. This workshop emphasizes learning through hands-on collaboration with AI rather than following predetermined steps. You'll make critical architectural decisions while the AI provides technical expertise and validates your choices against DynamoDB best practices.

This human-in-the-loop approach ensures you understand the reasoning behind each design decision while building practical experience with NoSQL data modeling principles.

## Starting Your Design Session

Let's begin by telling Cline to start working on data modeling. Use this command:

```shell
Please open this file `prompts/02-dynamodb-data-modeling/tasks.md` and start working in the first available task.
```

![Start conversation](/static/images/modernizr/2/stage02-01.png)

## Watching the Magic Happen

You'll know the workshop is working because you'll see Cline actively creating new files in real-time! It uses a visual diff system (like track changes in a document) to show you exactly what's being added or modified. This helps you understand each step of the process.

![Gitdiff](/static/images/modernizr/2/stage02-02.png)

**Take your time** with each file that gets generated. Don't rush through this process! Read everything, understand what Cline is doing at each step and why, and don't hesitate to ask questions. This is interactive learning - if you get confused at any point, just ask Cline to explain what's happening.

## Understanding the Variables

Generative AI is by nature non deterministic. Some "temperature" or variability in an LLMs answers allows it to be more creative in problem solving. Because of this, every design session is unique, so what you see might be slightly different from someone else's experience. That's normal and expected! Instead of giving you exact screenshots to match, we'll provide guidance on the important concepts and decisions you'll encounter.

One crucial thing to remember: **we need to support all 48 different access patterns** that were identified in Stage 1. Make sure this gets communicated clearly to Cline throughout the process.

## Providing Traffic Information

Cline will likely ask you about expected traffic patterns — basically, "How many people will be using this system?" Here's the information you should provide when asked:

```shell
Our best marketing estimates put us with 1400 Queries per second. 

Authentication and User management represent about 20% of the traffic, We are expecting to have 250 login operations per second (this includes our projections for growth), Registration is about 10 per second and profile management another 10.

Shopping cart operations are expected to be 25% of the traffic, where we have about 350 QPS for cart modifications and 250 QPS for people that is just viewing their shopping cart. 

Product Browsing and Search is the core of our traffic, 60% of it or 840 QPS, where we will have product search with 420 QPS, product listing with 420 and product details with 200 QPS. This is complemented by Categories operations that represents 15% of the traffic, where we expect to have 180 QPS for category navigation and 30 QPS for category searches. 

Order processing is the critical part of our business! this is what it generates the money, we are expecting to have 220 QPS representing about 15% of the traffic. Order creation 200 QPS, checkout validation 200 QPS and order management 120 QPS. 

Finally a very small set of operations are allocated to sellers, it is less than 1 QPS, representing 0.1% of the traffic. Maybe 0.05 QPS on product management, and 0.25 QPS on seller profiles, there is very low traffic on category management as they barely change.
```

![Questions](/static/images/modernizr/2/stage02-03.png)

## The Collaborative Design Process

As you work through this stage, you'll encounter several "checkpoint" moments where Cline stops and asks for your input. These aren't interruptions - they're important collaboration points designed to ensure the design stays on track and meets your specific needs.

![Start conversation](/static/images/modernizr/2/stage02-05.png)

## Being Patient with AI

During this intensive design stage, you might occasionally see messages about rate limiting or throttling. This is normal! Simply wait a few seconds and try again. The system can handle about 4 requests per minute, which should be enough for our workshop. If your task fails to execute please re-try, and just ignore the message that says "Try breaking down the task into smaller steps" as this is not our case, we know it is rate limiting!

![Start conversation](/static/images/modernizr/2/stage02-06.png)

## Using Specialized AI Tools

At some point, Cline will ask for permission to use the DynamoDB MCP Server — this is like accessing a specialized AI consultant who's an expert specifically in DynamoDB design. When asked, give permission for this. This expert AI will help analyze all the data we've collected and create a proper database design.

![Start conversation](/static/images/modernizr/2/stage02-07.png)

## Quality Control Checkpoint

Cline will first create a summary file called `dynamodb_requirements.md`. This is like having an architect show you the summary of everything you've discussed before they start drawing the blueprints.

::alert[ **Important:** Read this file carefully! Sometimes AI can accidentally add requirements that were never discussed, or miss important details. This is your chance to catch any errors before they become part of the final design.]{type="info"}

![Start conversation](/static/images/modernizr/2/stage02-08.png)

## Your First Database Design

Once you approve the requirements summary, Cline will create your actual DynamoDB data model. This is exciting — you're seeing your new database structure come to life! Cline has generated the new data model file `artifacts/stage-02/dynamodb_data_model.md` please open it and read it carefully.

![Start conversation](/static/images/modernizr/2/stage02-09.png)

## What Comes Next

After getting your initial design, the next step is validation — making sure this design is actually good and not just something that sounds impressive but won't work in practice. We'll examine the design carefully to ensure it's based on real requirements rather than AI imagination.

Remember, this is a collaborative process where your input and decisions shape the final outcome. You're learning to be a database architect while the AI handles the technical implementation details!
