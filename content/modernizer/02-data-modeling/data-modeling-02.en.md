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

We'll use their email address as the main identifier (called PK or Primary Key) because everyone has a unique email. Then we'll add a special tag called `#META` (that's our SK or Sort Key) to indicate this contains all the user's basic information (Metadata).

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
- These help us find users by their old ID numbers and usernames while we're switching systems. We will use the `user_id` as the partition key and sort key. This is for legacy support only. 
- For the second GSI we will keep the `username` as partition key and sort key, again used only for legacy support while we complete the migration. 
- Think of them as temporary bridges while we move from the old way to the new way

**GSI-3: Order Finder**
- This lets us quickly find any order just by its order number
- Like having a master list of all orders organized by order number

We could have been more efficient and combined some of these search helpers, but for this workshop, we're keeping them separate to make the code easier to understand and work with.

Now it's time to put our design into action! We need to provide all this information to our AI assistant (Cline) so it can start building our new database structure. Since we've been working on this for a while, we need to give it the complete context of what we're trying to accomplish.

## Setting Up the Data Model - What to Tell Your AI Assistant

When you're ready to create this database structure, you'll need to provide your AI assistant (like Cline) with all the details we've discussed. Here's exactly what information to share:

```shell
Users Table:
We will have a single table that will support multiple entities, using generic Partition Key `PK` and Sort Key `SK`.
- **Partition Key**: `PK = <user_email>`. Notice it is not prefixed with any text, this will allow direct authentication and groups all user-related data. 
- **Sort keys**: It is based on the different entities:
    - `SK = #META` - User profile and authentication data. User entity
    - `SK = CART#<product_id>` - Shopping cart items. Shoping cart entity
    - `SK = ORDER#<isodate>#<order_id>` - Stores orders with chronological sorting. Order Entity.

**USER Entity** (`PK = <user_email>`, `SK = #META`):
- `PK` (S): user email
- `SK` (S): #META
- `username` (S): unique username
- `email` (S): user email
- `password_hash` (S): authentication credential
- `profile_data` (M): flexible profile information
- `is_seller` (BOOL): seller capability flag
- `seller_profile` (M): seller-specific data
- `created_at` (S): ISO timestamp
- `updated_at` (S): ISO timestamp
- `status` (S): active/inactive

**SHOPPING CART Entity** (`PK = <user_email>`, `SK = CART#<product_id>`):
- `PK` (S): user email
- `SK` (S): CART#<product_id>
- `product_id` (S): product identifier
- `quantity` (N): item quantity
- `price` (N): price at add time
- `product_name` (S): denormalized product name
- `seller_id` (S): denormalized seller info
- `created_at` (S): ISO timestamp
- `updated_at` (S): ISO timestamp

**ORDER Entity** (`PK = <user_email>`, `SK = ORDER#<isodate>#<order_id>`):
- `PK` (S): user email
- `SK` (S): ORDER#<created_at>#<order_id>
- `user_id` (S): customer identifier (migration support)
- `order_status` (S): pending/confirmed/shipped/delivered
- `total_amount` (N): order total
- `order_items` (L): denormalized product details
- `shipping_address` (M): delivery information
- `payment_info` (M): payment method (encrypted)
- `seller_orders` (M): orders grouped by seller
- `created_at` (S): ISO timestamp
- `updated_at` (S): ISO timestamp
- `order_id` (S): UUID

### GSI1: Legacy User ID Support (Migration Only)
- **Purpose**: Temporary support for legacy user_id-based queries during migration phase
- **Partition Key**: `GSI1PK = <user_id>` - Legacy user identifier lookup, no prefix
- **Sort Key**: `GSI1SK = <user_id>` - Simple user mapping, no prefix
- **Projection**: ALL - Complete user data access during migration

### GSI2: Username Lookup (Migration Only)  
- **Purpose**: Username-based queries and uniqueness validation during migration
- **Partition Key**: `GSI2PK = username` - Username lookup capability
- **Sort Key**: `GSI2SK = username` - Direct username mapping
- **Projection**: ALL - Complete user data for username-based access

### GSI3: Order Lookup
- **Purpose**: Direct order retrieval by order ID for customer service and order management
- **Partition Key**: `GSI3PK = <order_id>` - Order identifier lookup
- **Sort Key**: `GSI3SK = <order_id>` - Direct order mapping  
- **Projection**: ALL - Complete order data for management operations
```

:image[User entity modification]{src="/static/images/modernizer/2/LGAM-02-stage02-11a.png" disableZoom=false width=425}

Make sure all the modifications are stored in the `working_log.md` file! sometimes `Cline` ignores what you say!!

Moving forward the output might be different given the undeterministc nature of LLMs, in some scenarios the models don't include all the attributes, in others, you have to explain it needed to create the GSIs. It is your responsibility to make sure every access patterns is properly identified and recorded, remember this is the base of data modeling and all the future steps depend on the decisions you make at this point. 

:image[User entity modification]{src="/static/images/modernizer/2/LGAM-02-stage02-11b.png" disableZoom=false width=425}

Before completing this workshop section, make sure the content you approve is valid, we are trying to use one table with 3 different entities, one for User metadata, another for User cart items and finally one for User orders! If in your case you are still getting suggestions to have another table for orders or shopping cart items, make sure you tell `Cline` we don't need it anymore. 

:image[User entity modification]{src="/static/images/modernizer/2/LGAM-02-stage02-12.png" disableZoom=false width=425}


