+++
title = "Step 3 - Create the Lambda function"
date = 2019-12-02T12:34:06-08:00
weight = 3
+++

This AWS Lambda function will attach to the DynamoDB Stream of the `logfile` table to replicate item puts and deletes to the `logfile_replica` table. The Lambda function code has been provided for you in the file `ddbreplica_lambda.py`. You may review the contents of the script if you would like with `vim` or `less`.

Zip the contents of the script. We will upload this to AWS Lambda when we create the function.
```bash
zip ddbreplica_lambda.zip ddbreplica_lambda.py lab_config.py
```
Get the Amazon Resource Name (ARN) of the precreated IAM role so that you can associate it with the Lambda function. Run the following command to retrieve the ARN of the role that was created during the lab creation.
```bash
cat ~/workshop/ddb-replication-role-arn.txt
```
The output looks like the following.
```txt
arn:aws:iam::<ACCOUNTID>:role/XXXXX-DDBReplicationRole-XXXXXXXXXXX
```
Now, copy the ARN from the output in place of the placeholder `YOUR_ARN_HERE` and run the following command to create the Lambda function.
```bash
aws lambda create-function \
--function-name ddbreplica_lambda --zip-file fileb://ddbreplica_lambda.zip \
--handler ddbreplica_lambda.lambda_handler --timeout 60 --runtime python3.7 \
--description "Sample lambda function for dynamodb streams" \
--role YOUR_ARN_HERE
```
