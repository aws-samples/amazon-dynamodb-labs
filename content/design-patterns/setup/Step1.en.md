---
title: "Step 1 - Open the AWS Systems Manager Console "
date: 2019-12-02T10:07:45-08:00
weight: 10
---

During the first 60 seconds, the environment will automatically update extensions and plugins. Any startup notification can be safely dismissed. 
 
![VS Code Setup](/static/images/common/common-vs-code-01.png)

If a terminal is not available at the bottom left side of your screen, please open a new one like the following picture indicates.

![VS Code Setup](/static/images/common/common-vs-code-02.png)

Then run the command `aws sts get-caller-identity` just to verify that your AWS credentials have been properly configured.

![VS Code Setup](/static/images/common/common-vs-code-03.png)

Change your directory to use LADV and browse the content:

```shell 
cd LADV
```

```shell
participant:~/workshop/LADV$ ls
data                  iam-trust-relationship.json  load_logfile_parallel.py          query_responsecode.py     scan_logfile_simple.py
ddbreplica_lambda.py  lab_config.py                query_city_dept.py                requirements.txt
gsi_city_dept.json    load_employees.py            query_employees.py                scan_for_managers.py
gsi_manager.json      load_invoice.py              query_index_invoiceandbilling.py  scan_for_managers_gsi.py
iam-role-policy.json  load_logfile.py              query_invoiceandbilling.py        scan_logfile_parallel.py
participant:~/workshop/LADV$ 
```
