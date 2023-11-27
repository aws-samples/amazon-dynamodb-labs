---
title: "6. View past games"
menuTitle: "View past games"
date: 2021-04-21T07:33:04-05:00
weight: 60
chapter: true
description: "In this module, you handle the final access pattern — find all past games for a user. Users in the application might want to view games they’ve played to watch replays, or they might want to view their friend's games."
---

In this module, you handle the final access pattern — find all past games for a user. Users in the application might want to view games they’ve played to watch replays, or they might want to view their friends’ games.

### Inverted index pattern

You might recall that there is a many-to-many relationship between the `Game` entity and the associated `User` entities, and the relationship is represented by a `UserGameMapping` entity.

Often, you want to query both sides of a relationship. With the primary key setup, you can find all the `User` entities in a `Game`. You can enable querying all `Game` entities for a `User` by using an *inverted index*.

In DynamoDB, an inverted index is a global secondary index (GSI) that is the inverse of your primary key. The sort key becomes your partition key and vice versa. This pattern flips your table and allows you to query on the other side of your many-to-many relationships.

In the following steps, you add an inverted index to the table and see how to use it to retrieve all `Game` entities for a specific `User`.
