---
title: "Step 4 - Check the content of the workshop folder"
date: 2019-12-02T10:07:55-08:00
weight: 40
---

On the Visual Studio Code terminal, go to the workshop folder and run the ls command:

```bash
cd /home/participant/workshop/LADV
ls -l .
```

The following list indicates the folder structure and the files that will be used during the workshop:

```bash

participant:~/workshop/LADV$ ls -l .
total 80
drwxr-xr-x. 2 participant participant  182 Oct 29 16:30 data
-rw-r--r--. 1 participant participant 1275 Sep 10 22:37 ddbreplica_lambda.py
-rw-r--r--. 1 participant participant  438 Sep 10 22:37 gsi_city_dept.json
-rw-r--r--. 1 participant participant  438 Sep 10 22:37 gsi_manager.json
-rw-r--r--. 1 participant participant  865 Sep 10 22:37 iam-role-policy.json
-rw-r--r--. 1 participant participant  205 Sep 10 22:37 iam-trust-relationship.json
-rw-r--r--. 1 participant participant   94 Sep 10 22:37 lab_config.py
-rw-r--r--. 1 participant participant 3845 Sep 10 22:37 load_employees.py
-rw-r--r--. 1 participant participant 2198 Sep 10 22:37 load_invoice.py
-rw-r--r--. 1 participant participant 1763 Sep 10 22:37 load_logfile.py
-rw-r--r--. 1 participant participant 3101 Sep 10 22:37 load_logfile_parallel.py
-rw-r--r--. 1 participant participant 1466 Sep 10 22:37 query_city_dept.py
-rw-r--r--. 1 participant participant 1071 Sep 10 22:37 query_employees.py
-rw-r--r--. 1 participant participant 2547 Sep 10 22:37 query_index_invoiceandbilling.py
-rw-r--r--. 1 participant participant 2341 Sep 10 22:37 query_invoiceandbilling.py
-rw-r--r--. 1 participant participant 1887 Sep 10 22:37 query_responsecode.py
-rw-r--r--. 1 participant participant   32 Sep 10 22:37 requirements.txt
-rw-r--r--. 1 participant participant 1287 Sep 10 22:37 scan_for_managers.py
-rw-r--r--. 1 participant participant 1157 Sep 10 22:37 scan_for_managers_gsi.py
-rw-r--r--. 1 participant participant 2019 Sep 10 22:37 scan_logfile_parallel.py
-rw-r--r--. 1 participant participant 1278 Sep 10 22:37 scan_logfile_simple.py
participant:~/workshop/LADV$ 
```

Python code:

- ddbreplica_lambda.py
- load_employees.py
- load_invoice.py
- load_logfile_parallel.py
- load_logfile.py
- lab_config.py
- query_city_dept.py
- query_employees.py
- query_index_invoiceandbilling.py
- query_invoiceandbilling.py
- query_responsecode.py
- scan_for_managers_gsi.py
- scan_for_managers.py
- scan_logfile_parallel.py
- scan_logfile_simple.py

JSON:

- gsi_city_dept.json
- gsi_manager.json
- iam-role-policy.json
- iam-trust-relationship.json

Text (used later in the lab):

- ddb-replication-role-arn.txt

Run the ls command to show the sample data files:

```bash
ls -l ./data
```

./data contents:

- employees.csv
- invoice-data2.csv
- invoice-data.csv
- logfile_medium1.csv
- logfile_medium2.csv
- logfile_small1.csv
- logfile_stream.csv

::alert[_Note: The code provided is for instructional use only. It should not be used outside of this lab, and it is not fit for production use._]{type="warning"}
