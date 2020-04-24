+++
title = "Sparse Global Secondary Indexes"
date = 2019-12-02T10:17:48-08:00
weight = 6
chapter = true
pre = "<b>Exercise 5: </b>"
description = "Learn how to cut down the resources required for your searches on uncommon attributes."
+++


You can use a sparse global secondary index to locate table items that have an uncommon attribute. To do this, you take advantage of the fact that table items that do not contain global secondary index attribute(s) are not indexed at all.

Such a query for table items with an uncommon attribute can be efficient because the number of items in the index is significantly lower than the number of items in the table. In addition, the fewer table attributes you project into the index, the fewer write and read capacity units you consume from the index.
