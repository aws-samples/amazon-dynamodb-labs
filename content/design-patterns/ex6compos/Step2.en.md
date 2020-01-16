+++
title = "Step 2 - Querying all the employees from a state"
date = 2019-12-02T12:16:25-08:00
weight = 2
+++

We can use the new GSI to query the table. If we are using only the state the query will not use the sort key attribute. But if the query has a value for the second parameter, the code will use the attribute **GSI_3_SK** of the GSI, which holds the same value as the **city_dept** attribute, to query all the values that begin with the parameter value.

**Figure - Using Composite key attributes to query by city and department**
![Using Composite key attributes to query by city and department](/images/awsconsole7.png)

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
Run the following Python script:
```bash
python query_city_dept.py employees TX
```
Output:
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
