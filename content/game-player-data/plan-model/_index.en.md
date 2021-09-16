+++
title = "Plan your data model"
menuTitle = "Plan your data model"
date = 2021-04-21T07:33:04-05:00
weight = 20
chapter = true
pre = "<b>2. </b>"
description = "In this module, you learn about DynamoDB data modelling best practices and review application access patterns."
+++

**Data modeling** is the process of designing how an application stores data in a given database. With a NoSQL database such as DynamoDB, data modeling is different than modeling with a relational database. A relational database is built for flexibility and can be a great fit for analytical applications. In relational data modeling, you start with your entities first. When you have a [normalized](https://en.wikipedia.org/wiki/Database_normalization) relational model, you can satisfy any query pattern you need in your application. 

NoSQL databases are designed for speed and scale — not flexibility. Though the performance of your relational database may degrade as you scale up, horizontally scaling databases such as DynamoDB provides consistent performance at any scale. Some DynamoDB users have tables that are larger than 100 TB, and the read and write performance of their tables is the same as when the tables were smaller than 1 GB in size. 

Achieving best results with a NoSQL database such as DynamoDB requires a shift in thinking from the typical relational database. 

Let's take a look at some of the best practices when modeling data with DynamoDB.

