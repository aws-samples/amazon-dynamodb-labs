+++
title = "Bank Payments Scenario"
chapter = false
weight = 2
+++

## NoSQL Design: Bank Payments Scenario

A Bank has asked you to develop a new backend system to handle their scheduled payments.

This is primarily an OLTP workload with daily batch processes. Items in the table(s) represent payments that are scheduled between accounts.  As items are inserted they are scheduled on a specific date to have the payment processed. Each day, items are regularly sent to a transactional system for processing, at which time their status changes to pending. Upon a successful transaction, an item’s status is set to processed and updated with a new transaction ID.

Workload Dimensions:

- Accounts can have multiple payments scheduled for any day in the future.
- Payments have the following data fields: *AccountID*, *ScheduledDate*, *Status* (`SCHEDULED`, `PENDING` or `PROCESSED`), *DataBlob* (*total size is < 8 KB*)
- There are 1 million automated scheduled payments added every day at 1:00 am–*for that day*, which need to complete in 30 minutes.
- There are 1 million payments added every day with the `SCHEDULED` state mostly in the hours of 6am-6pm
- During the day, a batch job runs regularly to query for today's `SCHEDULED` payments. This service will send the `SCHEDULED` items to the transaction service. Upon sending to the transaction service, the payment status is changed to `PENDING`.
- When the transaction service completes, the status of an item is changed to `PROCESSED` and a new transaction ID is added to the item.
- Items need to be returned for a specific account that are scheduled for payment in the next 90 days.
- The transactional service needs to retrieve all items for a specific date (i.e. today) across all accounts. It needs to be able to retrieve items that are specifically `SCHEDULED` or `PENDING`.

Develop a NoSQL data model for the bank fulfilling the scheduled payments requirements.

_Bonus challenge_:

- At the end of each day, all of the items which were `PROCESSED` need to be moved to a long term table (*due to compliance the data needs to be in a separate table*)

Design a second data model that fulfills that same access requirements as above, there is another access requirement which is to return a specific item associated with a transactionID.
