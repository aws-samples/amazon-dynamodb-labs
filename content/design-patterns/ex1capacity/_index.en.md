+++
title = "DynamoDB Capacity Units and Partitioning"
date = 2019-12-02T10:16:44-08:00
weight = 2
chapter = true
pre = "<b>Exercise 1: </b>"
+++


In this exercise you will load data into DynamoDB tables that are provisioned with different Write/Read capacity units, and compare the load times for different data sets. First, we will load a smaller data set to a table and note down the quick execution times. Next we will load a larger dataset to an under-provisioned table to simulate throttling exceptions. Next, we will simulate the GSI back pressure on a table by creating a table with higher provisioning and a GSI with only 1 WCU. You will be using the "service access log" data.
