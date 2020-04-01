+++
title = "Step 3 - Load a larger file to compare the execution times"
date = 2019-12-02T10:26:29-08:00
weight = 4
+++


Run the script again, but this time use a larger input data file.
```bash
python load_logfile.py logfile ./data/logfile_medium1.csv
```
**Parameters:** 1) Table name = `logfile` 2) File name = `logfile_medium1.csv`

The output will look like the following. It will run slower toward the end and take anywhere from one to three minutes to complete, depending on how quickly you run this command after Step 2.

```txt
row: 100 in 0.490761995316
...
row: 2000 in 3.188856363296509
RowCount: 2000, Total seconds: 75.0764648914
```

OR:

```txt
row: 100 in 0.490761995316
...
row: 2000 in 18.479122161865234
RowCount: 2000, Total seconds: 133.84829711914062
```

**Review the output:** You will notice that the load time for each batch of 100 rows was frequently above five seconds. This is because in each multisecond batch, you are seeing throttles that cause the Boto3 SDK to slow down the rate of inserts (also known as exponential backoff). The Boto3 SDK is waiting for DynamoDB to replenish the capacity of the DynamoDB table, which occurs every second for provisioned throughput tables. In Amazon CloudWatch, these throttles appear under the metric name `WriteThrottleEvents`.
