---
title: "2.2 Entities Design - Users"
menuTitle: "Entities Design - Users"
date: 2025-09-02T16:43:04-05:00
weight: 33
chapter: false
---

Think of designing database entities like organizing your closet. Instead of throwing everything in randomly, you want to group related items together so you can find what you need quickly. This is exactly what we're doing with our data - we're taking information that belongs together and storing it in the same place.

In NoSQL databases like DynamoDB, we have can use "denormalization." This means we can copy some information into multiple places to make our queries faster. It's like writing your friend's phone number in multiple notebooks so you can always find it quickly, no matter which notebook you're using.

## The User Entity - Our Digital ID Card

Let's start with the most important piece: **the user**. Think of this as a digital ID card that contains everything we need to know about a person using our application.

We'll use their email address as the main identifier (called PK or Primary Key) because everyone has a unique email. Then we'll add a special tag called `#META` (that's our SK or Sort Key) to indicate this contains all the user's basic information.

| What We Store | Type of Data | Why We Need It |
|---------------|--------------|----------------|
| PK | Text | The person's email address |
| SK | Text | "#META" (like a label saying "this is user info") |
| username | Text | Their chosen display name |
| email | Text | Their email address (same as PK) |
| password_hash | Text | Their password (encrypted for security) |
| profile_data | Collection | Things like birthday, interests, etc. |
| is_seller | True/False | Can they sell things on our platform? |
| seller_profile | Collection | Extra info if they're a seller |
| created_at | Text | When they joined |
| updated_at | Text | When they last changed something |
| status | Text | Are they active or inactive? |

**Why do we need extra search methods (GSIs)?**

During our transition from the old system to the new one, we need to be able to find users in multiple ways. It's like having multiple indexes in a library - you might want to find a book by title, author, or subject. We create these extra search methods (called GSIs - Global Secondary Indexes) so we can still find users by their old ID numbers or usernames while we're switching everything over.

## The Shopping Cart Entity - Your Digital Shopping Basket

Imagine you're walking through a store with a shopping basket. You'll select various quantities of different items to add to your cart. That's exactly what our shopping cart entity does digitally, except instead of a phyical item its a small note representing what is what is being purchased and in what quantity.

We link each cart item to the person's email (PK) and give each item a special label that starts with `CART#` followed by the product ID (SK).

| What We Store | Type of Data | Why We Need It |
|---------------|--------------|----------------|
| PK | Text | The shopper's email |
| SK | Text | "CART#" + the product's ID number |
| product_id | Text | Which product this is |
| quantity | Number | How many they want |
| price | Number | How much it cost when they added it |
| product_name | Text | The name of the product (copied for quick access) |
| seller_id | Text | Who's selling it (copied for quick access) |
| created_at | Text | When they added it to cart |
| updated_at | Text | When they last changed the quantity |

The beauty of this design is that we only care about each person's own shopping cart - we don't need to search through everyone else's carts. It's like your personal storage space - you only need access to your own stuff, not everyone else's.

## The Orders Entity - Your Purchase History

When someone actually buys something, we create an order record. Think of this like a receipt that keeps track of everything about the purchase. We organize these by the customer's email and create a special identifier that includes the date and a unique order number.

| What We Store | Type of Data | Why We Need It |
|---------------|--------------|----------------|
| PK | Text | The customer's email |
| SK | Text | "ORDER#" + date + order number |
| user_id | Text | Customer identifier |
| order_status | Text | Is it pending, shipped, delivered, etc.? |
| total_amount | Number | How much they paid in total |
| order_items | List | All the products they bought |
| shipping_address | Collection | Where to send it |
| payment_info | Collection | How they paid (kept secure) |
| seller_orders | Collection | Orders organized by which seller |
| created_at | Text | When they placed the order |
| updated_at | Text | When something changed |
| order_id | Text | Unique order number |

**Our Search Helpers (GSIs Explained Simply)**

Sometimes we need to find information in different ways, like when a customer calls and says "I have order number 12345, where is my package?" We need to be able to find that order quickly just from the order number.

**GSI-1 & GSI-2: Temporary Helpers for Migration**
- These help us find users by their old ID numbers and usernames while we're switching systems
- Think of them as temporary bridges while we move from the old way to the new way

**GSI-3: Order Finder**
- This lets us quickly find any order just by its order number
- Like having a master list of all orders organized by order number

We could have been more efficient and combined some of these search helpers, but for this workshop, we're keeping them separate to make the code easier to understand and work with.

Now it's time to put our design into action! We need to provide all this information to our AI assistant (Cline) so it can start building our new database structure. Since we've been working on this for a while, we need to give it the complete context of what we're trying to accomplish.

## Setting Up the Data Model - What to Tell Your AI Assistant

When you're ready to create this database structure, you'll need to provide your AI assistant (like Cline) with all the details we've discussed. Here's exactly what information to share:

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

![User entitiy modifcation](/static/images/modernizr/2/stage02-11.png)

Make sure all the modifications are stored in the `working_log.md` file! sometimes `Cline` ignores what you say!!

![Working Log](/static/images/modernizr/2/stage02-12.png)

In my specific scenario, `Cline` was having a hard time understanding it needed to create the GSIs and it wasn't including them in the data model. It is your responsibility to make sure every access patterns is properly identified and recorded, remember this is the base of data modeling and all the future steps depend on the decisions you make at this point. 

![Working Log](/static/images/modernizr/2/stage02-13.png)

Even at some points it actually suggested me to have a different table for my shopping cart entity. 

![Working Log](/static/images/modernizr/2/stage02-14.png)

But with a little patience, and making sure all the data is there I was able to guide `Cline` to obtain the outcome and table structure that we originally intended. 

![Working Log](/static/images/modernizr/2/stage02-15.png)

Before completing this workshop section, make sure the content you approve is valid, we are trying to use one table with 3 different entities, one for User metadata, another for User cart items and finally one for User orders! If in your case you are still getting suggestions to have another table for orders or shopping cart items, make sure you tell `Cline` we don't need it anymore. 



