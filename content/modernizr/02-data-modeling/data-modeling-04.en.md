---
title: "2.4 Entities Design - Categories"
menuTitle: "Entities Design - Categories"
date: 2025-09-02T16:43:04-05:00
weight: 35
chapter: false
---

## The Categories Table - Our Digital Department Store

Imagine walking into a huge department store. At the entrance, you see big signs pointing to major sections like "Electronics," "Clothing," and "Home & Garden." When you go to Electronics, you find smaller signs for "Computers," "Gaming," and "Mobile Phones." And if you go to Computers, you see even more specific sections like "Laptops," "Desktops," and "Accessories."

This is exactly what we're building with our categories table - a digital version of those department store signs that help people find what they're looking for. But instead of physical signs, we're creating a smart system that knows how all these categories connect to each other.

## Understanding the Family Tree Structure

Categories work like a family tree, but upside down. At the top, you have the "grandparent" categories (like Electronics), then "parent" categories (like Computers), and finally "child" categories (like Gaming Laptops). This is called a hierarchical structure - a fancy way of saying "organized levels."

In our system, we store two types of category information:

1. **Root Categories** - The big department signs (Electronics, Clothing, etc.)
2. **Child Categories** - All the smaller, more specific categories that belong under the big ones

## How We Organize This Information

Just like our other tables, we use the same smart organizing system with PK (Primary Key) and SK (Sort Key):

**For Root Categories:**
- PK = "ROOT" (a special label meaning "this is a top-level category")  
- SK = category name (like "Electronics")

**For Child Categories:**
- PK = parent category name (like "Electronics")
- SK = category name (like "Computers")

## What Information Do We Store About Each Category?

Here's everything we track for each category in our digital department store:

| What We Store | Type of Data | Why We Need It |
|---------------|--------------|----------------|
| PK | Text | Parent category name (or "ROOT" for main departments) |
| SK | Text | This category's name |
| parent_name | Text | What category this belongs under |
| category_name | Text | The display name people see |
| category_path | Text | The full path (like "Electronics > Computers > Laptops") |
| level | Number | How deep in the tree (0 = top level) |
| children_count | Number | How many subcategories this has |
| product_count | Number | How many products are in this category |
| created_at | Text | When this category was created |

## Making Categories Easy to Navigate - Our Search Helper

We need one main search method (GSI) to help people navigate through our category tree:

### GSI-1: Category Family Tree Navigator
This search helper lets us quickly find:
- All the main department categories (the "ROOT" categories)
- All subcategories under any parent category
- Any specific category by its ID (for migration from the old system)

Think of it like having a smart directory at the mall entrance that can instantly tell you:
- "Show me all the main departments"
- "Show me everything under Electronics"
- "Find the Gaming category for me"

## The Tricky Part - Handling "No Parent" Categories

Here's where things get a bit technical, but stick with me. In the old database system (MySQL), when a category didn't have a parent (meaning it was a top-level category), it was marked as "NULL" - basically meaning "empty" or "no parent."

With DynamoDB instead of leaving it empty, we use the word "ROOT" to mean "this is a top-level category."

**The Translation:**
- **Old System:** "This category has no parent" = NULL
- **New System:** "This category has no parent" = "ROOT"

This means when we move data from the old system to the new one, our code needs to automatically change any "no parent" categories to use "ROOT" instead.

## Why This Design Works So Well

This structure gives us amazing flexibility:
- Customers can browse by department, then drill down to exactly what they want
- Store managers can easily see how many products are in each category
- We can add new subcategories anywhere in the tree without breaking anything
- The system automatically keeps track of the full path to any category

It's like having a smart filing system that automatically organizes itself and can tell you exactly where everything belongs in the grand scheme of things.

## Setting Up the Categories Table - Instructions for Your AI Assistant

When creating this table, make sure your AI assistant understands:

**Key Design Points:**
1. Use "ROOT" for all top-level categories (PK = "ROOT")
2. Use the parent category name as PK for all child categories
3. Include the GSI for hierarchical navigation
4. Remember to translate NULL parent values to "ROOT" during migration
5. Keep track of children_count and product_count for performance

This categories system is the backbone of how customers will find products, so getting the structure right is crucial for a smooth shopping experience.


This is the prompt you should send. 

```shell
Categories table updates
This table contains two entities, it uses single table design as well. 

Parent category entity: **ROOT Categories (PK = ROOT, SK = category_name)**
Child category entity: **CHILD Categories (PK = parent_category_name, SK = category_name)**

| Attribute | Type | Purpose |
|-----------|------|---------|
| PK | String | parent_category_name (ROOT for root categories) |
| SK | String | category_name |
| parent_name | String | Parent category name (null for roots) |
| category_name | String | Category display name |
| category_path | String | Full hierarchy path |
| level | Number | Hierarchy level (0 = root) |
| children_count | Number | Number of child categories |
| product_count | Number | Number of products |
| created_at | String | ISO timestamp |

{
 "PK": "ROOT",
 "SK": "Electronics",
 "category_id": "1",
 "category_name": "Electronics",
 "category_path": "Electronics",
 "children_count": 2,
 "created_at": "2023-01-01T00:00:00.000Z",
 "GSI1PK": "ROOT",
 "GSI1SK": "1",
 "level": 0,
 "parent_id": null,
 "parent_name": null,
 "product_count": 0
}

{
 "PK": "Electronics",
 "SK": "Laptops",
 "category_id": "7",
 "category_name": "Laptops",
 "category_path": "Electronics/Laptops",
 "children_count": 0,
 "created_at": "2025-08-14 21:16:06",
 "GSI1PK": "1",
 "GSI1SK": "7",
 "level": 1,
 "parent_id": "1",
 "parent_name": "Electronics",
 "product_count": 0
}

GSI1: Category Hierarchy Lookup (Migration Support)

* Purpose: Enable hierarchical category queries by parent ID and direct category ID lookups for migration compatibility
* Partition Key: GSI1PK = parent_id (or "ROOT" for root categories) - Groups child categories under parent
* Sort Key: GSI1SK = category_id - Individual category identifier
* Projection: ALL - Complete category data for hierarchical access
* Sparse: No - All categories have parent relationships (ROOT for roots)
* Access Patterns Served:
    * Find child categories by parent ID (AP22: GSI1PK = parent_id)
    * Direct category lookup by ID (AP24: GSI1SK = category_id)
    * Root categories lookup (AP21: GSI1PK = "ROOT")
* Capacity Planning: 210 RPS reads for hierarchical and ID-based category access
* Migration Critical: Supports both hierarchical navigation and legacy ID-based lookups
```

Always remember to check if the input was added in the working log and the instructions were followed.

![Working Log](/static/images/modernizr/2/stage02-17.png)

Make sure that everything that is not needed, such other tables that might have been suggested before are not longer there, we don't need to send noise when we will re-generate the data model. 

![Working Log](/static/images/modernizr/2/stage02-18.png)

At this point `Cline` should tell you the summary of the work, and that it has effectively created a 3 table architecture. 

![Working Log](/static/images/modernizr/2/stage02-19.png)
