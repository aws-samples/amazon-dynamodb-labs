+++
title = "Composite Keys"
date = 2019-12-02T10:17:57-08:00
weight = 7
chapter = true
pre = "<b>Exercise 6: </b>"
description = "Learn how to combine two attributes into one to take advantage of the DynamoDB sort key."
+++


Carefully choosing the sort key attribute is important because it can significantly improve the selectivity of the items retrieved by a query. Let's say you need to create an application to query the employees by geographic location (state and city) and by department. You have the attributes: `state`, `city`, and `dept`. You can create a global secondary index that will combine these attributes to allow queries by location/dept. In DynamoDB you can query the items using a combination of the partition key and the sort key. In this case, your query criteria need to use more than two attributes, so you will create a composite-key structure that allows you to query with more than two attributes.

Previously (Exercise 4, Step 1) you ran commands to create the `employees` table and load it with sample records. One of the attributes in this data is called `state`, that stores two-letter state abbreviations for US states. In addition, the attribute value of state is prefixed with `state#` and stored under the attribute name `GSI_3_PK`. The script also created the attribute city_dept which represents a composite attribute using the `city` and `dept` attributes delimited by a # between the values. The attribute value uses the format `city#dept` (for example `Seattle#Development`). This attribute value is duplicated and stored under the `GSI_3_SK` key.


#### GSI_3

| Attribute Name (Type)        | Special Attribute?           | Attribute Use Case          | Sample Attribute Value  |
| ------------- |:-------------:|:-------------:| -----:|
| `GSI_3_PK` (STRING)      | GSI_3 partition key | The state of the employee  | `state#WA`  |
| `GSI_3_SK` (STRING)      | GSI_3 sort key | The city and department of the employee, concatenated  | `Seattle#Development`  |


**Note**: Though you’re making a new global secondary index for this query, you can still overload this global secondary index in the future. Global secondary index overloading gives you the flexibility to put different entity types in the same index (for example, employees and buildings). To support future growth, the `GSI_3` partition key is suffixed with the entity type, which allows you to insert rows in the same global secondary index later without comingling data.
