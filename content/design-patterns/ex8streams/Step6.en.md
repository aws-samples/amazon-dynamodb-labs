+++
title = "Step 6 - Populate the logfile table and verify replication to logfile_replica"
date = 2019-12-02T12:34:07-08:00
weight = 6
#TODO add link to issues at the end on GH
+++


Run the Python code to load more items into the table:
```bash
python load_logfile.py logfile ./data/logfile_stream.csv
```
Output:
```txt
RowCount: 2000, Total seconds: 15.808809518814087
```

#### Verify replication

You can scan the table **logfile_replica** to verify that the records have been replicated. It takes a few seconds, so you may need to repeat the following command until you get the records. Once again, use the up-arrow to repeate the previous command.
```bash
aws dynamodb scan --table-name 'logfile_replica' --max-items 2 --output text
```
You will see the first 2 items of the replica table as follows:
```txt
None    723     723
BYTESSENT       2969
DATE    2009-07-21
HOST    64.233.172.17
HOUROFDAY       8
METHOD  GET
REQUESTID       4666
RESPONSECODE    200
TIMEZONE        GMT-0700
URL     /gwidgets/alexa.xml
USERAGENT       Mozilla/5.0 (compatible) Feedfetcher-Google; (+http://www.google.com/feedfetcher.html)
BYTESSENT       1160
DATE    2009-07-21
HOST    64.233.172.17
HOUROFDAY       6
METHOD  GET
REQUESTID       4119
RESPONSECODE    200
TIMEZONE        GMT-0700
URL     /gadgets/adpowers/AlexaRank/ALL_ALL.xml
USERAGENT       Mozilla/5.0 (compatible) Feedfetcher-Google; (+http://www.google.com/feedfetcher.html)
NEXTTOKEN       eyJFeGNsdXNpdmVTdGFydEtleSI6IG51bGwsICJib3RvX3RydW5jYXRlX2Ftb3VudCI6IDJ9
```
**Note**: *Your log entries may differ. So long as you have two log entries, you've verified successful replication. If you don't see any entries, re-run the load_logfile.py command - you may have run the inserts too soon after creating the AWS Lambda function.*

## Congratulations, you have successfully completed all the exercises in the workshop.

**Questions? If you're in the room please raise your hand and ask. Thanks for attending!**
