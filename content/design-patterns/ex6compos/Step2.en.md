+++
title = "Step 2 - Query all the employees from a state"
date = 2019-12-02T12:16:25-08:00
weight = 2
+++

You can use the new global secondary index to query the table. If you use only the state, the query does not use the sort key attribute. However, if the query has a value for the second parameter, the code uses the `GSI_3_SK` attribute of the global secondary index, which holds the same value as the `city_dept` attribute, to query all the values that begin with the parameter value.

The following screenshot shows using composite key attributes to query by city and department.
![Using Composite key attributes to query by city and department](/images/awsconsole7.png)

We can perform this same query in a Python script.  This snippet shows how a script can take two input parameters (shown as value1 and value2) and craft a query against the GSI_3 global secondary index.

```py
if value2 == "-":
  ke = Key('GSI_3_PK').eq("state#{}".format(value1))
else:
  ke = Key('GSI_3_PK').eq("state#{}".format(value1)) & Key('GSI_3_SK').begins_with(value2)

response = table.query(
  IndexName='GSI_3',
  KeyConditionExpression=ke
  )
```

Run the following Python script to query global secondary index `GSI_3` for all employees in the state of Texas.

```bash
python query_city_dept.py employees TX
```
The result should look similar to the following.
```txt
List of employees . State: TX
    Name: Bree Gershom. City: Austin. Dept: Development
    Name: Lida Flescher. City: Austin. Dept: Development
    Name: Tristam Mole. City: Austin. Dept: Development
    Name: Malinde Spellman. City: Austin. Dept: Development
    Name: Giovanni Goutcher. City: Austin. Dept: Development
  ...
  Name: Cullie Sheehy. City: San Antonio. Dept: Support
  Name: Ari Wilstead. City: San Antonio. Dept: Support
  Name: Odella Kringe. City: San Antonio. Dept: Support
Total of employees: 197. Execution time: 0.238062143326 seconds
```

