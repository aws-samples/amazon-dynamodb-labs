+++
title = "Retail Cart Scenario"
chapter = false
weight = 1
+++

##  Retail Cart Challenge

An online retail store has asked you to design their data storage layer and NoSQL table(s). The website serves users and the products they view, save, and purchase. The website traffic is currently low, but they want to be able to serve millions of concurrent users.

- Users work with items that can be `ACTIVE`, `SAVED`, or `PURCHASED`. Once they are `PURCHASED` they will be assigned an *OrderId*.
- Items have the following: *AccountID*, *Status* (`ACTIVE`/`SAVED`/`PURCHASED`), *CreateTimestamp*, & *ItemSKU* - (Total size is < 1 KB)
- When a user logs in they view the active items in their cart – organized by most recently added.
- Users can view items that they have saved for later – organized by most recently saved items.
- Users can view items that they have purchased – also organized by most purchased saved items.
- Product teams have the ability to regularly query across all users to identify the users that have a specific product either `ACTIVE`, `SAVED`, or `PURCHASED`.
- The Business Intelligence team needs to run a number of ad hoc complex queries against the dataset to create weekly and monthly reports.

Build a NoSQL Data Model to fulfill the OLTP component of the workload. How you would fulfill the BI team’s requirement?
