+++
title = "Step 6 - Preload the items for the table Scan exercise"
date = 2019-12-02T10:20:18-08:00
weight = 60
+++



*Reminder: All commands are executed in your shell on the EC2 instance, not your local machine.*

In the upcoming Exercise #2 we will discuss table scan and its best practices. In this step, let's populate the table with 1 million items in preparation for that exercise.

Run the command to create a new table:
```bash
aws dynamodb create-table --table-name logfile_scan \
--attribute-definitions AttributeName=PK,AttributeType=S AttributeName=GSI_1_PK,AttributeType=S AttributeName=GSI_1_SK,AttributeType=S \
--key-schema AttributeName=PK,KeyType=HASH \
--provisioned-throughput ReadCapacityUnits=5000,WriteCapacityUnits=5000 \
--tags Key=workshop-design-patterns,Value=targeted-for-cleanup \
--global-secondary-indexes "IndexName=GSI_1,\
KeySchema=[{AttributeName=GSI_1_PK,KeyType=HASH},{AttributeName=GSI_1_SK,KeyType=RANGE}],\
Projection={ProjectionType=KEYS_ONLY},\
ProvisionedThroughput={ReadCapacityUnits=3000,WriteCapacityUnits=5000}"
```
This command will create a new table and one GSI with the following definition:

#### Table: logfile_scan

- Key schema: HASH
- Table RCU = 5000
- Table WCU = 5000
- GSI(s):
  - GSI_1 (3000 RCU, 5000 WCU) - *Allows for parallel or sequential scans of the access logs. Sorted by status code and timestamp.*


| Attribute name (Type)        | Special attribute?           | Attribute use case          | Sample attribute value  |
| ------------- |:-------------:|:-------------:| -----:|
| PK (STRING)      | Hash key | Holds the request id for the access log  | *request#104009*  |
| GSI_1_PK (STRING)      | GSI 1 hash key | A shard key, with values 0-N, to allow log searches  | *shard#3*  |
| GSI_1_SK (STRING)      | GSI 1 sort key | Sorts the logs hierarchically, from status code -> date -> hour  | *200#2019-09-21#01*  |

Run the command to wait until the table becomes Active:
```bash
aws dynamodb wait table-exists --table-name logfile_scan
```

#### Populate the table

Run the following command to load the server logs data into the logfile_scan table. It will load 1,000,000 rows to the table.
```bash
nohup python load_logfile_parallel.py logfile_scan &
disown
```

```nohup``` is used to run the process in the background, and ```disown``` allows the load to continue in case you are disconnected.

*Note: The following command will take about ten minutes to complete. It will run in the background.*



Run ```pgrep -l python``` to verify the script is loading data in the background.

```bash
pgrep -l python
```
Output:
```txt  
3257 python
```
*Note the process id - the 4 digit number in the above example - will be different for everyone.*

The script will continue to run in the background while you work on the next exercise.

**You have completed the SETUP!**
