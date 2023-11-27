---
title: "Build your entity-relationship diagram"
menuTitle: "ER diagram (ERD)"
date: 2021-04-21T07:33:04-05:00
weight: 22
chapter: false
description: "To get started, you configure your environment and download code that you use during the lab."
---

The first step of any data modeling exercise is to build a diagram to show the entities in your application and how they relate to each other.

In the application, you have the following entities:

- `User`

- `Game`

- `UserGameMapping`

A `User` entity represents a user in the application. A user can create multiple `Game` entities, and the creator of a game will determine which map is played and when the game starts. A `User` can create multiple `Game` entities, so there is a one-to-many relationship between `Users` and `Games`.

Finally, a `Game` contains multiple `Users` and a `User` can play in multiple different `Games` over time. 

Thus, there is a many-to-many relationship between `Users` and `Games`. You can represent this relationship with the `UserGameMapping` entity.

With these entities and relationships in mind, the entity-relationship diagram is shown below.

![ERD](/static/images/game-player-data/plan-model/erd.png)

Next, we will take a look at the access patterns the data model needs to support.