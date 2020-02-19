+++
title = "Step 4 - Check the content of the workshop folder"
date = 2019-12-02T10:07:55-08:00
weight = 40
+++


On the EC2 instance, go to the workshop folder and run the ls command:

```bash
cd /home/ec2-user/workshop
ls -l .
```

You will see the following content:

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

*Note: The code provided is for instructional use only. It should not be used outside of this lab, and it is not fit for production use.*
