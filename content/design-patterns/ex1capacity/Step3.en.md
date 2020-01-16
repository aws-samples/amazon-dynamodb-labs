+++
title = "Step 3 - Load a larger file to compare the execution times"
date = 2019-12-02T10:26:29-08:00
weight = 4
+++


Run the script again but at this time with a larger input data file:
```bash
python load_logfile.py logfile ./data/logfile_medium1.csv
```
Parameters: 1) Table Name = **logfile** 2) File Name = **logfile_medium1.csv**

The output will look like this - it will run slower towards the end and take anywhere from one to three minutes to complete, depending on how quickly you run this command after the previous step:

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

**Review the output**: *You will notice that the load time for each batch of 100 rows was frequently above 5 seconds. This is related to exponential backoffs by the boto3 SDK in response to throttles from DynamoDB. In each multi-second batch, we are seeing throttles that cause the SDK to slow down the rate of inserts. The time is higher in some batches because the boto3 SDK is sleeping, waiting for DynamoDB to replenish the token buckets of the DynamoDB table.*
