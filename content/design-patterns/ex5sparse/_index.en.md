+++
title = "Sparse Global Secondary Indexes"
date = 2019-12-02T10:17:48-08:00
weight = 6
chapter = true
pre = "<b>Exercise 5: </b>"
+++


You can use a sparse global secondary index to efficiently locate table items that have an uncommon attribute. To do this, you take advantage of the fact that table items that do not contain global secondary index attribute(s) are not indexed at all.

Such a query can be very efficient because the number of items in the index will be significantly fewer than the number of items in the table. In addition, the fewer table attributes you project into the index, the fewer write and read capacity units you will consume from the index.
