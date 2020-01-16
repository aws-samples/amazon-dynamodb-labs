+++
title = "Step 2 - Load data to the new table"
date = 2019-12-02T10:50:03-08:00
weight = 2
+++


You will now execute a script that will load the data from the file named ./employees.csv into the table named "employees".

The sample employees.csv record looks like the below:
```csv
1000,Nanine Denacamp,Programmer Analyst,Development,San Francisco,CA,1981-09-30,2014-06-01,Senior Database Administrator,2014-01-25
```
When we ingest this data into the table, we will concatenate some of the attributes, such as city_dept (example: San Francisco:Development) because we have an access pattern in our query that will take advantage of this concatenated attribute. The "colA" attribute is also a derived attribute. All of this concatenation is handled in the python script where the record is assembled, and then executes a put_item() to write the record to the table.
```bash
python load_employees.py employees ./data/employees.csv
```
Output:
```txt
$ python load_employees.py employees ./data/employees.csv
employee count: 100 in 3.7393667697906494
employee count: 200 in 3.7162938117980957
...
employee count: 900 in 3.6725080013275146
employee count: 1000 in 3.6174678802490234
RowCount: 1000, Total seconds: 36.70457601547241
```
Take a look on the DynamoDB table 'employees' using the AWS console: (On the console, click on the table "employees" on the left, and on the right side pane, select the "Items" tab.

**Figure - Employees table**
![Employees table](/images/awsconsole4a.png)

#### GSI_1

On the same page, in the right hand pane, select the dropdown item that says [Index] and click Start Search.

**Figure - Searching the GSI**
![Searching the GSI](/images/awsconsole5.png)

**Figure - Global Secondary Index content**
![Global Secondary Index](/images/awsconsole6.png)
