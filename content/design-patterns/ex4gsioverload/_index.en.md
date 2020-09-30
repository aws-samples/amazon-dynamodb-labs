+++
title = "Global Secondary Index Key Overloading"
date = 2019-12-02T10:17:33-08:00
weight = 5
chapter = true
pre = "<b>Exercise 4: </b>"
description = "Explore how to maintain the ability to query on many attributes when you have a multi-entity table."
+++


You can create 20 global secondary indexes for a DynamoDB table as of the time this page was written. Sometimes, though, your application might need to support multiple access patterns and exceed the current limit of global secondary indexes per table. The global secondary index key overloading design pattern is enabled by designating and reusing an attribute name (column header) across different item types and storing a value in that attribute depending on the context of the item type. When you create a global secondary index on that attribute, you are indexing for multiple access patterns, each for a different item type—and have used only 1 global secondary index. For example, an `employees` table. An employee can contain items of type `metadata` (for employee details), `employee-title` (all the job titles that the employee has held), or `employee-location` (all the office buildings and locations where the employee has worked).

The access patterns required for this scenario are:

- Query all employees of a state
- Query all employees with one specific current title
- Query all employees who had ever one specific title
- Query employees by name

The following screenshot shows the design of the `employees table`. The attribute called `PK` has the employee ID, which is prefixed by the letter `e`. The hash sign (#) is used as a separator between the entity type identifier (`e`) and the actual employee ID. The `SK` is  an overloaded attribute, and has either current title, previous title, or the keyword `root`, which denotes the primary item for the employee that holds most of their important attributes. The `GSI_1_PK` attribute includes the title or the name of the employee. The re-use of a given global secondary index for multiple entity types such as employees, employee locations, and employee titles lets us simplify our management of the DynamoDB table because we only need to monitor and pay for one global secondary index as opposed to three separate indexes.


![Sample design for the Employees table using the GSI overloading pattern](/images/awsconsole4.png)
