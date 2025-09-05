---
title: "2.1 Data modeling"
menuTitle: "Data modeling"
date: 2025-09-02T16:43:04-05:00
weight: 32
chapter: false
---

## Design Process Continuation and Context Management

During the data modeling phase, you may encounter context window limitations as the system accumulates extensive analysis data. When Cline prompts for a new task initiation, this indicates the conversation has reached capacity limits. This is standard behavior in AI-assisted development workflows. Your progress remains preserved through the working log and task files, ensuring continuity across sessions.

## Proceeding to Validation Phase (Task 3.1)

If the system doesn't automatically advance to task 3.1, manually initiate the next phase:

```shell
Great please continue with task 3.1 available here prompts/02-dynamodb-data-modeling/tasks.md
```

## Access Pattern Validations

Task 3.1 implements a validation step that verifies your DynamoDB design supports all identified access patterns from the requirements analysis. This validation process serves as a quality assurance checkpoint, detecting potential AI-generated artifacts that don't correspond to actual system requirements — a common issue in AI-assisted development where models may extrapolate beyond provided specifications.

Following validation, you'll receive a table-by-table analysis of your data model. Before proceeding, review the generated design document at `artifacts/stage-02/dynamodb_data_model.md` to understand the proposed architecture.

::alert[Pro-TIP! for an easier visualization right click on the file and select open preview]{type="info"}
::alert[Given the non-deterministic nature of GenAI the data model might be different for everyone that is running this workshop. Some of them might have gotten a single table design and other closer to normalization (basically SQL in NoSQL which we don't want). ]{type="warning"}

## Data Relationship Analysis

Rather than following prescriptive instructions, focus on understanding the core data modeling concepts underlying your e-commerce application. Analyzing entity relationships and data dependencies is fundamental to creating an effective NoSQL design that supports all required access patterns.

This picture is an Entity Relationship Mapping that will help you understand in detail what it needs to be modeled. 

![Start conversation](/static/images/modernizr/2/stage02-10.png)

## Entity Relationship Mapping

The e-commerce application presents several one-to-many relationships that inform the DynamoDB design strategy:

### Primary Relationship Patterns:

- **Users → Products**: One-to-many relationship where seller accounts can manage multiple product listings
- **Users → Orders**: One-to-many relationship supporting customer order history tracking
- **Users → Cart Items**: One-to-many relationship enabling persistent shopping cart functionality
- **Categories → Products**: One-to-many relationship for product categorization and navigation
- **Products → Order Items**: Many-to-many relationship through order items junction entity
- **Products → Cart Items**: Many-to-many relationship through cart items junction entity
- **Orders → Order Items**: One-to-many relationship for multi-item order support

## DynamoDB Entity Aggregation Strategy

These relationships reveal natural aggregation opportunities where related entities can be co-located within the same table partition. For instance, user-centric data including profile information, order history, and active cart contents share logical cohesion and similar access patterns. Generally a good mantra for data modeling in DynamoDB is that "data accessed together should be stored together".

## Partition Key Design Principles

DynamoDB lets you use real business attributes as partition keys instead of generated IDs. For example, using `user_email` as the key ensures each record is unique while also making it easier to organize and query data in ways that match how the application actually uses it.

For additional query flexibility during the migration phase, Global Secondary Indexes (GSI) can provide alternate access paths based on `userID` or `username` attributes without impacting primary table performance.

## Single Table Design Patterns

DynamoDB's strength lies in its ability to store heterogeneous entity types within a single table structure, provided they share logical relationships and similar access patterns. This approach, known as single table design, optimizes performance by co-locating related data and minimizing cross-table queries.

Example entity co-location for the Users table:
- **User Profile Entity**: Core user metadata and authentication information
- **User Order History**: Historical order records associated with the user
- **Active Cart Items**: Current shopping session state data

This co-location strategy enables efficient retrieval of all user-related information through single query operations, reducing read cost and improving performance.

## Implementation Considerations

The effectiveness of this design approach depends on carefully analyzing query patterns and ensuring that entity groupings align with actual application access requirements rather than traditional relational modeling conventions.
