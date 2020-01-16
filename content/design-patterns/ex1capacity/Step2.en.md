+++
title = "Step 2 - Load sample data into the table"
date = 2019-12-02T10:26:28-08:00
weight = 3
+++


The table is created. Let's load some sample data into the table by running the following Python script:
```bash
cd /home/ec2-user/workshop
python load_logfile.py logfile ./data/logfile_small1.csv
```
Parameters in the above command: 1) Table Name = **logfile** 2) File Name = **logfile_small1.csv**

The output will look like this:

```txt
row: 100 in 0.780548095703125
row: 200 in 7.2669219970703125
row: 300 in 1.547729730606079
row: 400 in 3.9651060104370117
row: 500 in 3.98996901512146
RowCount: 500, Total seconds: 17.614499807357788
```


**Curious behavior**: *You might be wondering why one of the runs took more than 5 seconds. Check out the next step to see this behavior explained.*
