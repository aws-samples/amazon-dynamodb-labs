---
title: "2.3 Entities Design - Products"
menuTitle: "Entities Design - Products"
date: 2025-09-02T16:43:04-05:00
weight: 34
chapter: false
---

## The Products Table - Our Digital Catalog

Now that we've designed how to store user information and their activities, we need a place to store all the products available in our marketplace. Think of this as creating a digital catalog, like those product catalogs you might get in the mail, but much smarter and more organized.

When your AI assistant (the LLM) first looked at this problem, it came up with a design that was pretty close to what we wanted. However, we're going to make a few small but important changes to make our system more flexible for the future.

## Why Are We Using PK and SK Instead of Just Product ID?

You might wonder why we're not just using `product_id` as our main identifier. The reason is like building a house with room to expand later. By using PK (Primary Key) and SK (Sort Key), we're creating space to add related information about each product in the future without having to rebuild our entire system. As a side benefit, shorter key names save storage too!

For now, our PK will be the product ID, and our SK will be `#META` (which means "this contains the main product information"). This setup is like having a filing cabinet where each product gets its own folder, and we can add different types of documents to that folder later.

## What Information Do We Store About Each Product?

Here's everything we need to track for each product in our marketplace:

| What We Store | Type of Data | Why We Need It |
|---------------|--------------|----------------|
| PK | Text | The unique product ID |
| SK | Text | "#META" (label for main product info) |
| product_id | Text | The same as PK (for easy reference) |
| seller_id | Text | Who is selling this product |
| category_id | Text | What category it belongs to (like "Electronics") |
| category_path | Text | The full category tree (like "Electronics > Laptops > Gaming") |
| product_name | Text | The product's title |
| description | Text | Details about what the product does |
| price | Number | How much it costs |
| inventory_quantity | Number | How many are available |
| image_url | Text | Link to the product's picture |
| search_terms | Text | Words people might use to find this product |
| created_at | Text | When it was first listed |
| updated_at | Text | When it was last changed |
| status | Text | Is it available or discontinued? |

## Making Products Easy to Find

Just like with users and orders, we need ways to find products quickly. We'll create two main search methods (GSIs):

### GSI-1: Finding Products by Category
This is like organizing products by department in a store. When someone wants to browse all laptops or all books, this index makes it super fast to find them. 

**Important Note:** Popular categories (like "Electronics") might get very busy, which could slow things down. It's like having everyone crowd into the most popular store section - we'll need to keep an eye on this.

### GSI-2: Finding Products by Seller  
This lets sellers quickly see all their products, and lets customers browse everything a particular seller offers. It's like having a directory of all the shops in a mall.

**Important Note:** Sellers with lots of products might create the same crowding issue as popular categories, so we'll monitor this too.

## What Makes This Design Flexible?

The beauty of our setup is that it's designed to grow. Right now, each product just has one record (the #META record with all its basic information). But later, we could add:

- Customer reviews (using the same product ID but different SK values)
- Price history tracking
- Inventory updates from different warehouses
- Product variants (different sizes, colors, etc.)

It's like starting with a basic photo album but designing it so you can easily add more sections later without having to reorganize everything.

## Setting Up the Products Table - Instructions for Your AI Assistant

When you're ready to create the products table, make sure your AI assistant understands these exact specifications. The attribute names must match exactly what's listed above - this is crucial for everything to work together properly.

**Key Points to Emphasize:**
1. Use PK = product_id and SK = #META for the main product record
2. Include both GSI-1 (for categories) and GSI-2 (for sellers)
3. Make sure all attribute names match the table above exactly
4. Set up monitoring for the GSIs since they could become busy with popular categories or high-volume sellers

The changes we're making are small adjustments to what the AI originally suggested, but these details matter a lot for making sure everything works smoothly together.

```shell
Products table updates

For simplicity let's have a table with PK = product_id and SK = #META this allow us future expansion if we need to start denormalizing the attributes. (MAKE SURE THE ATTRIBUTE NAME MATCHES WHAT IT SAYS HERE!!)

| Attribute | Type | Purpose |
|-----------|------|---------|
| PK | String | product_id |
| SK | String | #META |
| product_id | String | product_id |
| seller_id | String | Seller identifier |
| category_id | String | Category identifier |
| category_path | String | Full category hierarchy |
| product_name | String | Product title |
| description | String | Product description |
| price | Number | Current price |
| inventory_quantity | Number | Available quantity |
| image_url | String | Image URL |
| search_terms | String | Searchable text |
| created_at | String | ISO timestamp |
| updated_at | String | ISO timestamp |
| status | String | active/inactive |

{
 "PK": "6",
 "SK": "#META",
 "category_id": "11",
 "category_path": "Tools",
 "created_at": "2025-08-14 21:16:07",
 "description": "20V MAX cordless drill with 2 batteries, charger, and carrying case. 1/2-inch chuck, LED light, and 15 clutch settings.",
 "GSI1PK": "11",
 "GSI1SK": "Cordless Drill Kit",
 "GSI2PK": "1",
 "GSI2SK": "Cordless Drill Kit",
 "id": 6,
 "image_url": "https://images.unsplash.com/photo-1504148455328-c376907d081c?w=600&h=600&fit=crop&auto=format",
 "inventory_quantity": 19,
 "price": 129.99,
 "product_name": "Cordless Drill Kit",
 "seller_id": "1",
 "updated_at": "2025-08-17T15:05:47.840Z"
}

We will add two indexes, that are possible future hot partitions, but with the numbers that we have discussed so far, this will be fine for this design. 

**GSI-1: Category Products (Potential Hot Partition)**
- PK: GSI1PK = category_id, SK: GSI1SK = category_id
- Projection: ALL
- Purpose: Category-based browsing 
- **Warning:** Monitor for hot partitions with popular categories

**GSI-2: Seller Products (Potential Hot Partition)**
- PK: GSI2PK = seller_id, SK: GSI2SK = seller_id
- Projection: ALL
- Purpose: Seller product management
- **Warning:** Monitor for hot partitions with high-volume sellers
```

![Working Log](/static/images/modernizr/2/stage02-16.png)

In my execution, I was getting throttled, please remember to be patient and just retry! but also review the changes made by `Cline`.