---
title: "2. Scenario Overview"
date: 2023-12-01T00:00:00-00:00
weight: 5
chapter: true
---

Imagine you have an e-commerce website where customers place orders for different items. The website relies on Amazon DynamoDB and it requires logging of all events from when an order is placed until the item is delivered.

Website Requirements:

* The status of orders placed on your website can be `ACTIVE`, `PLACED`, `COMPLETE` or `CANCELLED`.
* You need to keep the current view of customers' orders on the main database table used by your application.
* Each order has a `status` attribute and contains a list of one or more items.

In JSON format, an item on the orders table has the following attributes.

![Order Profile](/static/images/change-data-capture/overview/order-profile.png)

You will implement a solution to meet this requirement by using two DynamoDB tables - Orders and OrdersHistory; and a streaming solution to copy item level changes from the Orders table to OrdersHistory table.
