+++
title = "Step 6 - Populate the logfile table and verify replication to logfile_replica"
date = 2019-12-02T12:34:07-08:00
weight = 6
+++


Run the following Python code to load more items into the `logfile` table. The rows will be copied to the DynamoDB stream, procecesed by the AWS Lambda function, and then writen into the `logfile_replica` table at the end.

```bash
python load_logfile.py logfile ./data/logfile_stream.csv
```
The output will look like the following.
```txt
RowCount: 2000, Total seconds: 15.808809518814087
```

#### Verify replication

You can scan the `logfile_replica` table to verify that the records have been replicated. It takes a few seconds, so you may need to repeat the following AWS CLI command until you get the records. Once again, use the up-arrow to repeat the previous command.

```bash
aws dynamodb scan --table-name 'logfile_replica' --max-items 2 --output text
```
You will see the first two items of the replica table as follows.
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
**Note**: Your log entries may differ. As long as you have two log entries, you've verified successful replication. If you don't see any entries, rerun the `load_logfile.py` command because you might have run the inserts too soon after creating the Lambda function.

## Congratulations, you have successfully completed all the exercises in the workshop!

If you ran the lab on your own AWS account, you should delete all the tables made during these exercises. If you are at an AWS event using the AWS Workshop platform (the Event Engine), you do not need to delete your tables.

#### Reporting issues

Firstly, if you encounter an issue running the lab that needs to be addressed we recommend you fork the code on GitHub and make a pull request with your change. Please review [our contributing guide on GitHub.com]({{% siteparam "github_contributing_guide" %}}).

Secondly, if you have a feature request or you are unable to fork the package to make a change yourself please submit [an issue on our GitHub page]({{% siteparam "github_issues_link" %}}).
