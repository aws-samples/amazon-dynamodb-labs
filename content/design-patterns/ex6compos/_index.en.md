+++
title = "Composite keys"
date = 2019-12-02T10:17:57-08:00
weight = 7
chapter = true
pre = "<b>Exercise 6: </b>"
+++


Careful selection of the Sort Key attribute is an important step because it can significantly improve the selectivity of the items retrieved by a query. Now, imagine you need to create an application to query the employees by geographic location (State and City) and by department. Considering you have the attributes: state, city, and dept. You can create a GSI that will combine them to allow the queries by location/dept. In DynamoDB you can query the items using a combination of the Partition Key and the Sort Key. In this case, your query criteria needs to use more than two attributes. So we will create a composite-key structure that will allow us to query using more than two attributes.

The table load script created an attribute called **state** that has the two digit state code. In addition, the attribute value of **state** is prefixed with 'state#' and stored under the attribute name **GSI_3_PK**. The script also created the attribute **city_dept** which represents a composite attribute using the two attributes city and dept delimited by a "#" between the values. The attribute values uses the format 'city#dept', for example 'Seattle#Engineering'. This attribute value is duplicated and stored under the key **GSI_3_SK**.

#### GSI: GSI_3

| Attribute name (Type)        | Special attribute?           | Attribute use case          | Sample attribute value  |
| ------------- |:-------------:|:-------------:| -----:|
| GSI_3_PK (STRING)      | GSI 3 hash key | The State of the employee  | *state#WA*  |
| GSI_3_SK (STRING)      | GSI 3 sort key | The city and department of the employee, concatenated  | *Seattle#Development*  |


**Note**: *While we're making a new GSI for this query, you can still overload this GSI in the future. GSI overloading gives you the flexibility to put different entity types in the same index, for example employees and buildings. To support future growth, we have suffixed the GSI 3 partition key with the entity type, which allows us to later insert rows in the same GSI without co-mingling data*
