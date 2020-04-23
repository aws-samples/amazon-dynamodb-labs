+++
title = "Step 3 - Create the Lambda function"
date = 2019-12-02T12:34:06-08:00
weight = 3
+++


The Lambda function has been provided for you. Zip the contents of the script.
```bash
zip ddbreplica_lambda.zip ddbreplica_lambda.py lab_config.py
```
Get the Amazon Resource Name (ARN) of the precreated IAM role so that you can associate it with the Lambda function.
```bash
cat ~/workshop/ddb-replication-role-arn.txt
```
The file was made during the creation and configuration of this lab. The output looks like the following.
```txt
arn:aws:iam::<ACCOUNTID>:role/XXXXX-DDBReplicationRole-XXXXXXXXXXX
```
Now, copy the ARN from the output in the following `–role` parameter and run the command to create the Lambda function.
```bash
aws lambda create-function \
--function-name ddbreplica_lambda --zip-file fileb://ddbreplica_lambda.zip \
--handler ddbreplica_lambda.lambda_handler --timeout 60 --runtime python3.7 \
--description "Sample lambda function for dynamodb streams" \
--role YOUR_ARN_HERE
```
