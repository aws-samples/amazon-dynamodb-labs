---
title: "Single table design"
date: 2021-04-21T07:33:04-05:00
weight: 10
---

## What is single table design?

Single table design is a DynamoDB modeling technique where you store multiple entity types in one table. Instead of creating separate tables for Users, Orders, and OrderItems (as you would in a relational database), you store them all in one table called `simple-inventory`.

## Why single table design?

DynamoDB is optimized for known access patterns. By co-locating related entities in a single table, you can:

- **Retrieve related data in a single query** - get a user and all their orders without joins
- **Reduce costs** - one table instead of multiple tables to manage
- **Use transactions across entities** - atomic operations spanning users and orders
- **Simplify operations** - one table to monitor, back up, and scale

The trade-off is that you must plan your access patterns upfront and design your keys carefully.

## Key design

You use prefixed composite keys to distinguish entity types. Every item has a `pk` (partition key) and `sk` (sort key):

| Entity | pk | sk |
|--------|----|----|
| User | `#USER#<username>` | `PROFILE` |
| Order | `#USER#<username>` | `#ORDER#<order-id>` |
| Order Item | `#ORDER#<order-id>` | `#ITEM#<item-id>` |

This design creates natural hierarchies:
- A user's profile and orders share the same partition key (`#USER#username`)
- An order's items share the same partition key (`#ORDER#order-id`)

## Access patterns

The following table shows every access pattern this workshop supports and which index serves it:

| # | Access Pattern | Index | Key Condition |
|---|---------------|-------|---------------|
| 1 | Get user profile | Primary | `pk=#USER#john AND sk=PROFILE` |
| 2 | Get user's orders | Primary | `pk=#USER#john AND begins_with(sk, #ORDER#)` |
| 3 | Get order items | Primary | `pk=#ORDER#uuid AND begins_with(sk, #ITEM#)` |
| 4 | Find order by ID | GSI: `inverted-index` | `sk=#ORDER#uuid` |
| 5 | Get pending orders | GSI: `placed-index` | `placed_id=pending` |
| 6 | Get user orders by status/date | LSI: `status-date-index` | `pk=#USER#john AND begins_with(status_date, pending#)` |
| 6b | Get user orders by status/date (multi-attribute keys) | GSI: `status-date-gsi` | `pk=#USER#john AND status=pending AND created_at > 2024-01-01` |

Access pattern 6 appears twice: once with a Local Secondary Index using a manually concatenated `status_date` key (the classic approach), and once with a Global Secondary Index using multi-attribute keys (a newer DynamoDB feature). You implement both so you can compare them in [Module 4](/dynamodb-for-go-developers/read-data).

## Index strategy

### Primary table (pk, sk)
Handles direct lookups and hierarchical queries. Because orders are stored under the user's partition key, you can fetch all of a user's orders with a single query.

### Global Secondary Index: `inverted-index` (sk → pk)
Reverses the key order. This lets you look up an order by its ID when you don't know which user placed it.

### Global Secondary Index: `placed-index` (placed_id)
A sparse index. Only items with a `placed_id` attribute appear in this index. Orders have this attribute only while they are in `pending` or `confirmed` status. Once shipped or delivered, the attribute is removed and the order disappears from the index.

### Local Secondary Index: `status-date-index` (pk, status_date)
Provides an alternate sort order within a user's partition. The `status_date` attribute is a composite string like `pending#2024-01-15`, which lets you query a user's orders by status and sort them chronologically. Building this composite string by hand is the classic workaround for querying on multiple dimensions.

### Global Secondary Index: `status-date-gsi` (pk, status, created_at) - multi-attribute keys
A newer alternative that uses **multi-attribute keys** (GSIs can compose a sort key from up to four separate attributes). Instead of concatenating `status` and the date into one string, this index uses `status` and `created_at` as two independent sort key attributes. You get the same access pattern without any string manipulation, and each attribute keeps its native type. You explore this feature in detail in Module 4.

::alert[The `status` and `created_at` attributes are already present on every order, so no data changes are needed to populate this index.]{type="info"}

## Entity examples

### User
```json
{
  "pk": "#USER#john",
  "sk": "PROFILE",
  "username": "john",
  "email": "john@example.com",
  "full_name": "John Doe",
  "addresses": {
    "home": {"street": "123 Main St", "state": "CA", "country": "USA"}
  }
}
```

### Order
```json
{
  "pk": "#USER#john",
  "sk": "#ORDER#550e8400-e29b-41d4-a716-446655440000",
  "order_id": "550e8400-e29b-41d4-a716-446655440000",
  "user_id": "john",
  "status": "pending",
  "status_date": "pending#2024-01-15",
  "placed_id": "pending",
  "address_key": "home",
  "created_at": "2024-01-15T10:30:00Z"
}
```

### Order Item
```json
{
  "pk": "#ORDER#550e8400-e29b-41d4-a716-446655440000",
  "sk": "#ITEM#item-001",
  "order_id": "550e8400-e29b-41d4-a716-446655440000",
  "item_id": "item-001",
  "name": "Laptop",
  "description": "Gaming laptop",
  "price": 1299.99,
  "quantity": 1
}
```

In the next step, you provision this table with all its indexes using CloudFormation.
