---
title: "2. Scenario Overview"
date: 2023-12-01T00:00:00-00:00
weight: 5
chapter: true
---

Imagine you have an e-commerce website where customers place orders for different items. The website is backed by Amazon DynamoDB and you need to keep a record of all events that occur from the moment an order is placed until all items on the order are delivered to the customer.

Orders placed on your website can have one of the follow statuses - `ACTIVE`, `PLACED`, `COMPLETE` or `CANCELLED`; but you only want to keep the current view of customers' orders on the main database table used by your application.

Each order has a list containing one of more order items. Each order item also has a status attribute.

In JSON format, an item on the orders table has the following attributes.

![Order Profile](/static/images/change-data-capture/overview/order-profile.png)

You will implement a solution to meet this requirement by using two DynamoDB tables - Orders and OrdersHistory; and a streaming solution to copy item level changes from the Orders table to OrdersHistory table.
