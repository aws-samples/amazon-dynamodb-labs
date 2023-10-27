---
title: "Global Secondary Indexes"
date: 2021-04-24T07:38:58-05:00
weight: 35
---

We have concerned ourself hitherto with accessing data based on the key attributes. If we wanted to look for items based on non-key attributes we had to do a full table scan and use filter conditions to find what we wanted, which would be both very slow and very expensive for systems operating at large scale.

DynamoDB provides a feature called [Global Secondary Indexes (GSIs)](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GSI.html) which will automatically pivot your data around different Partition and Sort Keys. Data can be re-grouped and re-sorted to allow for more access patterns to be quickly served with the Query and Scan APIs.

Remember the previous example where we wanted to find all the replies in the **Reply** table that were posted by User A and needed to use a `Scan` operation?  If there had been a billion **Reply** items but only three of them were posted by User A, we would have to pay (both in time and money) to scan through a billion items just to find the three we wanted.

Armed with this knowledge of GSIs, we can now create a GSI on the **Reply** table to service this new access pattern.  GSIs can be created and removed at any time, even if the table has data in it already! This new GSI will use the *PostedBy* attribute as the Partition (HASH) key and we will still keep the messages sorted by *ReplyDateTime* as the Sort (RANGE) key.  We want all the attributes from the table copied (projected) into the GSI so we will use the ALL ProjectionType.  Note that the name of the index we create is `PostedBy-ReplyDateTime-gsi`.  

Navigate to the **Reply** table, switch to the **Indexes** tab and click `Create Index`.

![Console Create GSI 1](/images/hands-on-labs/explore-console/console_create_gsi_1.png)

Enter `PostedBy` as the Partition key, `ReplyDateTime` as the Sort key, and `PostedBy-ReplyDateTime-gsi` as the Index name.  Leave the other settings as defaults and click `Create Index`.  Once the index leaves the `Creating` state you can continue on to the exercise below.

## Exercise

1. Find all the Replies written by User A sorted, using the console to issue a Query instead of a Scan.

Hint: When using a GSI in DynamoDB you have to explicitly tell DynamoDB to use the index instead of the table.

The solution is expandable below but try to figure it out yourself before moving forward.

**Click below to expand and see the exercise solutions**

{{%expand "Expand this to see the solution" %}}

1. Navigate to the Item Explorer for the **Reply** table. Running a Query on a GSI is no different than running it against a table, except we need to select the GSI we want to use for the Query and we'll use the GSI key attributes in the KeyConditionExpression.

Even if the table has a billion **Reply** items authored by other Users, this query will only cost us to read the exact 3 items we're hoping to return (unlike a `Scan`).

![Console Create GSI 2](/images/hands-on-labs/explore-console/console_create_gsi_2.png)

{{% /expand%}}

### Cleanup

When you're done, make sure to remove the GSI. Return to the Indexes tab, select the `PostedBy-ReplyDateTime-gsi` index and click `Delete`.

![Console Delete GSI](/images/hands-on-labs/explore-console/console_delete_gsi.png)
