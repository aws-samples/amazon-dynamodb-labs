+++
title = "Step 3 - Create the Lambda function"
date = 2019-12-02T12:34:06-08:00
weight = 3
+++


The Lambda function has been provided to you. Zip the contents of the script as follows:
```bash
zip ddbreplica_lambda.zip ddbreplica_lambda.py lab_config.py
```
Get the ARN of the pre-created IAM role so that we can associate it with the Lambda function:
```bash
cat ~/workshop/ddb-replication-role-arn.txt
```
The file was made during the creation and configuration of this lab. The output will be like:
```txt
arn:aws:iam::<ACCOUNTID>:role/XXXXX-DDBReplicationRole-XXXXXXXXXXX
```
Now, copy the ARN from the output in the --role parameter below and run the command to create the Lambda function:
```bash
aws lambda create-function \
--function-name ddbreplica_lambda --zip-file fileb://ddbreplica_lambda.zip \
--handler ddbreplica_lambda.lambda_handler --timeout 60 --runtime python3.7 \
--description "Sample lambda function for dynamodb streams" \
--role YOUR_ARN_HERE
```
