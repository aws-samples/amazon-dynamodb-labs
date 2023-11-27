---
title: "Review Access Patterns"
menuTitle: "Review Access Patterns"
date: 2021-04-21T07:33:04-05:00
weight: 23
chapter: false
description: "In this module, we look at different access patterns we need to model the data for."
---

Let's take a look at the different access patterns we need to model the data for.

### Consider user profile access patterns

The users of the gaming application need to create user profiles. These profiles include data such as a user name, avatar, game statistics, and other information about each user. The game displays these user profiles when a user logs in. Other users can view the profile of a user to review their game statistics and other details.

As a user plays games, the game statistics are updated to reflect the number of games the user has played, the number of games the user has won, and the number of kills by the user.

Based on this information, you have three access patterns:

- Create user profile (Write)
- Update user profile (Write)
- Get user profile (Read)


### Consider pre-game access patterns

The game is an online multiplayer game similar to [Fortnite](https://www.epicgames.com/fortnite) or [PUBG](https://www.pubg.com/). Players can create a game at a particular map, and other players can join the game. When 50 players have joined the game, the game starts and no additional players can join.

When searching for games to join, players may want to play a particular map. Other players won’t care about the map and will want to browse open games across all maps.

Based on this information, you have the following seven access patterns:

- Create game (Write)
- Find open games (Read)
- Find open games by map (Read)
- View game (Read)
- View users in game (Read) 
- Join game for a user (Write)
- Start game (Write)


### In-game and post-game access patterns

Finally, let’s consider the access patterns during and after a game.

During the game, players try to defeat other players with the goal of being the last player standing. The application tracks how many kills each player has during a game as well as the amount of time a player survives in a game. If a player is one of the last three surviving in a game, the player receives a gold, silver, or bronze medal for the game.

Later, players may want to review past games they’ve played or that other players have played.

Based on this information, you have three access patterns:

- Update game for user (Write)
- Update game (Write)
- Find all past games for a user (Read)


### Review

You have now mapped all access patterns for the gaming application. In the following modules, you implement these access patterns by using DynamoDB. 

Note that the planning phase might take a few iterations. Start with a general idea of the access patterns your application needs. Map the primary key, secondary indexes, and attributes in your table. Go back to the beginning and make sure all of your access patterns are satisfied. When you are confident the planning phase is complete, move forward with implementation.