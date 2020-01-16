+++
title = "Step 6 - Load more data with the new capacity"
date = 2019-12-02T10:26:29-08:00
weight = 7
+++


After the capacity is increased, run the Python script again to populate the table using **logfile_medium2.csv** with the same number of rows of the previous run. You will see that at this time the execution will be faster.
```bash
python load_logfile.py logfile ./data/logfile_medium2.csv
```
The output will look like this:
```txt
row: 100 in 0.9451174736022949
row: 200 in 0.8512668609619141
...
row: 1900 in 0.8499886989593506
row: 2000 in 0.8817043304443359
RowCount: 2000, Total seconds: 17.13607406616211
```
**Note:** *With the new capacity, the total load time is lower.*
