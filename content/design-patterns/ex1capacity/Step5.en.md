+++
title = "Step 5 - Increase the capacity of the table"
date = 2019-12-02T10:26:29-08:00
weight = 6
+++


Run the following AWS CLI command to increase the write capacity units and read capacity units from 5 to 100.
```bash
aws dynamodb update-table --table-name logfile \
--provisioned-throughput ReadCapacityUnits=100,WriteCapacityUnits=100
```

Run the command to wait until the table becomes Active.
```bash
time aws dynamodb wait table-exists --table-name logfile
```

**Topic for discussion:** How long did it take to increase the capacity? Was it faster, or longer than you expected? Often, when  you need more capacity from your provisioned throughput table it is available in only tens of seconds.
