+++
title = "Working with Table Scans"
date = 2020-04-21T07:38:58-05:00
weight = 33
+++

The [Scan API](https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_Scan.html) which can be invoked using the [scan CLI command](https://docs.aws.amazon.com/cli/latest/reference/dynamodb/scan.html). Scan will do a full table scan and return the items in 1MB chunks.

The Scan API is similar to the Query API except that since we want to scan the whole table and not just a single Item Collection, there is no Key Condition Expression for a Scan.  However, you can specify a [Filter Expression](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Scan.html#Scan.FilterExpression) which will reduce the size of the result set (even though it will not reduce the amount of capacity consumed).

Let us look at the data in the **Reply** table which has both a Partition Key and a Sort Key. Select the left menu bar **Explore items**.
![Console Menu Item Explorer](/images/hands-on-labs/explore-console/console_menu_explore_item.png)
You may need to click the hamburger menu icon to expand the left menu if its hidden.
![Console Menu Hamburger Icon](/images/hands-on-labs/explore-console/console_menu_hamburger_icon.png)


Once you enter the Explore Items you need to select the **Reply** table and then expand the Scan/Query items box.

![Item Explorer Expand Tables](/images/hands-on-labs/explore-console/console_explore_item_select_table.png)

For example, we could find all the replies in the Reply that were posted by User A.   

![Item Explorer Scan Reply 1](/images/hands-on-labs/explore-console/console_item_explorer_scan_reply_1.png)

You should see 3 **Reply** items posted by User A.

## Exercise

Explore the data in the *Forum* table and write a scan command to return only the Forums that have more than 1 thread and more than 50 views.

The solution is expandable below but try to figure it out yourself before moving forward.

**Click below to expand and see the exercise solutions**

{{%expand "Expand this to see the solution" %}}
For this access pattern we will need to make a FilterCondition with clauses on both the *Threads* and *Views* attributes before clicking **Run**.

![Item Explorer Scan Reply 2](/images/hands-on-labs/explore-console/console_item_explorer_scan_reply_2.png)

{{% /expand%}}
