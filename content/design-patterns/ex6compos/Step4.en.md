+++
title = "Step 4 - Querying all the employees of a city and a specific department"
date = 2019-12-02T12:16:26-08:00
weight = 4
+++

You also can use the global secondary index to query employees by state. Run the following Python script to list all employees in the Operation department in Dallas, Texas.
```bash
python query_city_dept.py employees TX --citydept 'Dallas#Op'
```
Output:
```txt
List of employees . State: TX
    Name: Brady Marvel. City: Dallas. Dept: Operation
    Name: Emmye Fletcher. City: Dallas. Dept: Operation
    Name: Audra Leahey. City: Dallas. Dept: Operation
    Name: Waneta Parminter. City: Dallas. Dept: Operation
    Name: Lizbeth Proudler. City: Dallas. Dept: Operation
    Name: Arlan Cummings. City: Dallas. Dept: Operation
    Name: Bone Ruggs. City: Dallas. Dept: Operation
    Name: Karlis Prisk. City: Dallas. Dept: Operation
    Name: Marve Bignold. City: Dallas. Dept: Operation
Total of employees: 9. Execution time: 0.174154996872 seconds
```
In this exercise, we created a global secondary index to query additional attributes. Data can now be retrieved using the City and Department fields.
