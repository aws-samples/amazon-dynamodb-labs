+++
title = "Retail Cart Scenario"
chapter = false
weight = 1
+++

##  Retail Cart Challenge

An online retail store has asked you to design their data storage layer and NoSQL table(s). The website serves users and the products they view, save, and purchase. The website traffic is currently low, but they want to be able to serve millions of concurrent users.

- Users work with items that can be `ACTIVE`, `SAVED`, or `PURCHASED`. Once they are `PURCHASED` they will be assigned an *OrderId*.
- Items have the following attributes: *AccountID*, *Status* (`ACTIVE`, `SAVED`, or `PURCHASED`), *CreateTimestamp*, & *ItemSKU* (Total item size is < 1 KB).
- When a user logs in, they view the active items in their cart, which are organized by most recently added.
- Users can view items that they have saved for later, which are organized by most recently saved.
- Users can view items that they have purchased, which are organized by most recently purchased.
- Product teams have the ability to regularly query across all users to identify the users that have a specific product that is either `ACTIVE`, `SAVED`, or `PURCHASED`.
- The Business Intelligence team needs to run a number of complex ad hoc queries against the dataset to create weekly and monthly reports.

Build a NoSQL Data Model to fulfill the OLTP component of the workload. How you would fulfill the BI team’s requirement?
