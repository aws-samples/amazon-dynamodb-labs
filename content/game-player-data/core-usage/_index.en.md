+++
title = "Core usage: user profiles and games"
menuTitle = "Core usage: user profiles and games"
date = 2021-04-21T07:33:04-05:00
weight = 30
chapter = true
pre = "<b>3. </b>"
description = "In this module, you design the primary key for the game application’s table, create the table and perform some basic actions."
+++

In the previous module, the game application’s access patterns were defined. In this module, the [primary key](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.CoreComponents.html#HowItWorks.CoreComponents.PrimaryKey) for the DynamoDB table is defined and the core access patterns are handled.

#### When designing the primary key for a DynamoDB table, keep the following best practices in mind:
- **Start with the different entities in your table.** If you are storing multiple different types of data in a single table—such as [employees, departments, customers, and orders](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-modeling-nosql-B.html) — be sure your primary key has a way to distinctly identify each entity and enable core actions on individual items.
- **Use prefixes to distinguish between entity types.** Using prefixes to distinguish between entity types can prevent collisions and assist in querying. For example, if you have both customers and employees in the same table, the primary key for a customer could be `CUSTOMER#<CUSTOMERID>`, and the primary key for an employee could be `EMPLOYEE#<EMPLOYEEID>`.
- **Focus on single-item actions first, and then add multiple-item actions if possible.** For a primary key, it’s important that you can satisfy the read and write options on a single item by using the single-item APIs: [GetItem](https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_GetItem.html), [PutItem](https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_PutItem.html), [UpdateItem](https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_UpdateItem.html), and [DeleteItem](https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_DeleteItem.html). You may also be able to satisfy your multiple-item read patterns with the primary key by using [Query](https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_Query.html). If not, you can add a secondary index to handle the `Query` use cases.


With these best practices in mind, let’s design the primary key for the game application’s table and perform some basic actions.