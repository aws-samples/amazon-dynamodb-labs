+++
title = "Step 3 - Query all the employees of a city"
date = 2019-12-02T12:16:25-08:00
weight = 3
+++


You have a new global secondary index that you can use for querying employees by city. Run the following Python command to list all employees by department in Dallas, Texas.
```bash
python query_city_dept.py employees TX --citydept Dallas
```
The result should look like the following.
```txt
List of employees . State: TX
    Name: Grayce Duligal. City: Dallas. Dept: Development
    Name: Jere Vaughn. City: Dallas. Dept: Development
    Name: Valeria Gilliatt. City: Dallas. Dept: Development
  ...
  Name: Brittani Hunn. City: Dallas. Dept: Support
    Name: Oby Peniello. City: Dallas. Dept: Support
Total of employees: 47. Execution time: 0.21702003479 seconds
```


