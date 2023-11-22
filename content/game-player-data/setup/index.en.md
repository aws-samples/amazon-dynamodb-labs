---
title: "Getting Started"
menuTitle: "Getting Started"
date: 2021-04-21T07:33:04-05:00
weight: 10
chapter: true
pre: "<b>1. </b>"
description: "In this module, you configure your environment and download code that you will use throughout the lab."
---

## Background

Imagine you are building an online multiplayer game similar to [Fortnite](https://www.epicgames.com/fortnite) or [PUBG](https://www.pubg.com/). 

In your game, groups of 50 players join a session to play a game, which typically takes around 30 minutes to play. During the game, you have to update a specific player’s record to indicate the amount of time the player has been playing, the number of kills they’ve recorded, or whether they won the game. Users want to see old games they’ve played, either to view the games’ winners or to watch a replay of each game’s action.

In this lab, we will learn how to model a DynamoDB table to handle the application’s access patterns. We will also learn some core data modeling strategies to use DynamoDB in a fast, high-performing way.

In this module, you'll configure your environment and download code that you will use throughout the lab.

## Getting Started

To set up this workshop, choose one of the following paths, depending on whether you are:

{{% notice warning %}}
If following the lab in your own AWS Account, you will create DynamoDB tables that will incur a cost that could approach tens of dollars per day. **Ensure you delete the DynamoDB tables using the DynamoDB console, and make sure you [delete the Cloud9 environment](https://docs.aws.amazon.com/cloud9/latest/user-guide/delete-environment.html) as soon as the lab is complete**.
{{% /notice %}}

- […running the workshop on your own (in your own AWS account)]({{< ref "/game-player-data/setup/on-your-own" >}}), which guides you to launch a Cloud9 environment using CloudFormation

- […attending an AWS-hosted event (using AWS-provided access-code)]({{< ref "/game-player-data/setup/aws-ws-event" >}})


Once you have completed with either setup, continue on to:
- [Step 1: Setup AWS Cloud9 IDE]({{< ref "/game-player-data/setup/step1" >}})
