---
title: "Design the primary key"
menuTitle: "Design the primary key"
date: 2021-04-21T07:33:04-05:00
weight: 31
chapter: false
description: "To get started, you configure your environment and download code that you use during the lab."
---

Let’s consider the different entities, as suggested in the preceding introduction. In the gaming application, you have the following entities:

- `User`
  
- `Game`
  
- `UserGameMapping`


A `UserGameMapping` is a record that indicates a user joined a game. There is a many-to-many relationship between `User` and `Game`.

Having a many-to-many mapping is usually an indication that you want to satisfy two `Query` patterns, and this gaming application is no exception. You have an access pattern that needs to find all users that have joined a game as well as another pattern to find all games that a user has played.

If your data model has multiple entities with relationships among them, you generally use a [composite primary](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.CoreComponents.html#HowItWorks.CoreComponents.PrimaryKey) key with both *partition key* and *sort key* values. The composite primary key gives you the `Query` ability on the *partition key* to satisfy one of the query patterns you need. In the DynamoDB documentation, the *partition key* is also called `HASH` and the *sort key* is called `RANGE`.

The other two data entities — `User` and `Game` — don’t have a natural property for the *sort key* value because the access patterns on a `User` or `Game` are a key-value lookup. Because a *sort key* value is required, you can provide a filler value for the *sort key*.

With this in mind, let’s use the following pattern for *partition key* and *sort key* values for each entity type.

Entity          | Partition Key   | Sort Key
----------------|-----------------|---------
User            | USER#\<USERNAME>| #METADATA#\<USERNAME>
Game            | GAME#<GAME_ID>  | #METADATA#<GAME_ID>
UserGameMapping | GAME#<GAME_ID>  | USER#\<USERNAME>

Let’s walk through the preceding table.

For the `User` entity, the *partition key* value is `USER#<USERNAME>`. Notice that a prefix is used to identify the entity and prevent any possible collisions across entity types.

For the *sort key* value on the `User` entity, a static prefix of `#METADATA#` followed by the `USERNAME` value is used. For the *sort key* value, it’s important that you have a value that is known, such as the `USERNAME`. This allows for single-item actions such as `GetItem`, `PutItem`, and `DeleteItem`. 

However, you also want a *sort key* value with different values across different `User` entities to enable [even partitioning](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.Partitions.html) if you use this attribute as a *partition key* for an index. For that reason, you append the `USERNAME`.

The `Game` entity has a primary key design that is similar to the `User` entity’s design. It uses a different prefix (`GAME#`) and a `GAME_ID` instead of a `USERNAME`, but the principles are the same.

Finally, the `UserGameMapping` uses the same partition key as the `Game` entity. This allows you to fetch not only the metadata for a `Game` but also all the users in a `Game` in a single query. You then use the `User` entity for the *sort key* on the `UserGameMapping` to identify which user has joined a specific game.

In the next step, you create a table with this primary key design.