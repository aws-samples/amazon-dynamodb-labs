+++
title = "Step 3 - Querying all the employees of a city"
date = 2019-12-02T12:16:25-08:00
weight = 3
+++


Now, you have a new GSI you can use for query employees by state. Run the following Python application:
```bash
python query_city_dept.py employees TX --citydept Dallas
```
Output:
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
