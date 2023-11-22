---
title: "Summary & Cleanup"
menuTitle: "Summary & Cleanup"
date: 2021-04-21T07:33:04-05:00
weight: 70
chapter: true
pre: "<b></b>"
description: "Final words"
---

In the previous modules, the following access patterns in the gaming application were handled:

- Create user profile (Write)
- Update user profile (Write)
- Get user profile (Read)
- Create game (Write)
- Find open games (Read)
- View game (Read)
- Join game for a user (Write)
- Start game (Write)
- Update game for a user (Write)
- Update game (Write)
- Find games for user (Read)

The strategies used to satisfy these patterns include:
- A single-table design that combines multiple entity types in one table.
- A composite primary key that allows for many-to-many relationships.
- A sparse global secondary index (GSI) to filter on one of the fields.
- DynamoDB transactions to handle complex write patterns across multiple entities.
- An inverted index (GSI) to allow reverse lookups on the many-to-many entity.

#### Congratulations! You made it to the end of this workshop.

Please take a few moments to share your feedback with us using the link that you received from the lab facilitator.


## Cleanup

If you were running this lab in your own AWS Account (not an AWS run event), don't forget to cleanup the resources, by deleting the CloudFormation stack or the resources themselves (incase of no CloudFormation stack) you used during setup.

::alert[If following the lab in your own AWS Account, you will create DynamoDB tables that will incur a cost that could approach tens or hundreds of dollars per day. **Ensure you delete the DynamoDB tables using the DynamoDB console, and make sure you [delete the Cloud9 environment](https://docs.aws.amazon.com/cloud9/latest/user-guide/delete-environment.html) as soon as the lab is complete**.]{type="warning"}