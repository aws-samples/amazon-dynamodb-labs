+++
title = "Solutions"
date = 2019-12-02T10:50:03-08:00
weight = 1
+++

```json

{
    "Version": "2012-10-17",
    "Statement": [
    {
        "Sid": "ReadFromDynamoDBStream",
        "Effect": "Allow",
        "Action": [
        "dynamodb:DescribeStream",
        "dynamodb:GetRecords",
        "dynamodb:GetShardIterator",
        "dynamodb:ListStreams"
        ],
        "Resource": "arn:aws:dynamodb:us-west-1:${AWS::AccountId}:table/ReduceTable/stream/*"
    },
    {
        "Sid": "CreateCloudwatchLogGroup",
        "Effect": "Allow",
        "Action": [
        "logs:CreateLogGroup"
        ],
        "Resource": "arn:aws:logs:us-west-1:${AWS::AccountId}:*"
    },
    
    {
        "Sid": "WriteToCloudwatchLogGroup",
        "Effect": "Allow",
        "Action": [
        "logs:CreateLogStream",
        "logs:PutLogEvents"
        ],
        "Resource": "arn:aws:logs:us-west-1:${AWS::AccountId}:log-group:/aws/lambda/ReduceLambda:*"
    },
    {
        "Sid": "WriteToDynamoDBTable",
        "Effect": "Allow",
        "Action": [
        "dynamodb:UpdateItem"
        ],
        "Resource": "arn:aws:dynamodb:us-west-1:${AWS::AccountId}:table/AggregateTable"
    },
    {
        "Sid": "ReadFromParameterTable",
        "Effect": "Allow",
        "Action": [
        "dynamodb:GetItem"
        ],
        "Resource": "arn:aws:dynamodb:us-west-1:${AWS::AccountId}:table/ParameterTable"
    }
    ]
}
```

# Lab 2 Solutions

## Lab 2 StateLambda function complete code
```python
# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

# --------------------------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------------------------

# General Imports
import json
import time
import base64
import random
from decimal import Decimal

# AWS Imports
import boto3
from botocore.exceptions import ClientError

# Project Imports
import functions
import constants

# --------------------------------------------------------------------------------------------------
# Lambda Function
# --------------------------------------------------------------------------------------------------

def lambda_handler(event, context):

    # Print Status at Start
    records = event['Records']
    print('Invoked StateLambda with ' + str(len(records)) + ' record(s).')

    # Initialize DynamoDB
    ddb_ressource = boto3.resource('dynamodb')
    table = ddb_ressource.Table(constants.STATE_TABLE_NAME)

    # Get Failure PCT
    FAILURE_STATE_LAMBDA_PCT = functions.get_parameter(ddb_ressource, "FAILURE_STATE_LAMBDA_PCT", 0)

    # Loop over records
    for record in records:

        # Manually Introduced Random Failure
        if random.uniform(0,100) < FAILURE_STATE_LAMBDA_PCT / len(records):
            # Raise exception
            raise Exception('Manually Introduced Random Failure!')

        # Load Record
        data = json.loads(base64.b64decode(record['kinesis']['data']).decode('utf-8'))

        # Get Entries
        record_id           = data[constants.ID_COLUMN_NAME]
        record_hierarchy    = data[constants.HIERARCHY_COLUMN_NAME]
        record_value        = data[constants.VALUE_COLUMN_NAME]
        record_version      = data[constants.VERSION_COLUMN_NAME]
        record_time         = data[constants.TIMESTAMP_COLUMN_NAME]

        # If Record is older than 1 Minute -> Ignore it
        if (time.time() - record_time) > 60:
            continue

        # Write to DDB
        try:
            table.update_item(
                Key = {
                    constants.STATE_TABLE_KEY: record_id
                    },
                ConditionExpression = 'attribute_not_exists(' + constants.STATE_TABLE_KEY + ') OR ' + constants.VERSION_COLUMN_NAME + '< :new_version',
                UpdateExpression = 'SET  #VALUE     = :new_value,' + \
                                        '#VERSION   = :new_version,' + \
                                        '#HIERARCHY = :new_hierarchy,' + \
                                        '#TIMESTAMP = :new_time',
                ExpressionAttributeNames={
                    '#VALUE':       constants.VALUE_COLUMN_NAME,
                    '#VERSION':     constants.VERSION_COLUMN_NAME,
                    '#HIERARCHY':   constants.HIERARCHY_COLUMN_NAME,
                    '#TIMESTAMP':   constants.TIMESTAMP_COLUMN_NAME
                    },
                ExpressionAttributeValues={
                    ':new_version':     record_version,
                    ':new_value':       Decimal(str(record_value)),
                    ':new_hierarchy':   json.dumps(record_hierarchy, sort_keys = True),
                    ':new_time':        Decimal(str(record_time))
                    }
                )
        except ClientError as e:
            if e.response['Error']['Code']=='ConditionalCheckFailedException':
                print('Conditional put failed.' + \
                    ' This is either a duplicate or a more recent version already arrived.')
                print('Id: ',           record_id)
                print('Hierarchy: ',    record_hierarchy)
                print('Value: ',        record_value)
                print('Version: ',      record_version)
                print('Timestamp: ',    record_time)
            else:
                raise e

    # Print Status at End
    print('StateLambda successfully processed ' + str(len(records)) + ' record(s).')
    return {'statusCode': 200}
```

## Lab 2 ReduceLambda function complete code
```python
# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

# --------------------------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------------------------

# General Imports
import json
import hashlib
import random
import time

# AWS Imports
import boto3
from botocore.exceptions import ClientError

# Project Imports
import functions
import constants

# --------------------------------------------------------------------------------------------------
# Lambda Function
# --------------------------------------------------------------------------------------------------

def lambda_handler(event, context):

    # Print Status at Start
    records = event['Records']
    print('Invoked ReduceLambda with ' + str(len(records)) + ' Delta message(s).')

    # Initialize Dict for Total Delta
    totals = dict()

    # Initialize DDB Ressource
    ddb_ressource = boto3.resource('dynamodb', region_name=constants.REGION_NAME)

    # Keep track of number of batches for timestamp mean
    batch_count = 0

    # Iterate over Messages
    for record in event['Records']:

        # Aggregate over Batch of Messages the Lambda was invoked with
        if 'NewImage' in record['dynamodb']:

            # Load Message to Dict
            message = record['dynamodb']['NewImage']['Message']['S'].replace("'",'"')
            data = json.loads(message)

            # Get Batch Count (To Calculate Mean of Timestamp)
            batch_count += 1

            # Iterate over Entries in Message
            for entry in data:
                if (entry == constants.TIMESTAMP_GENERATOR_FIRST or entry == constants.TIMESTAMP_GENERATOR_MEAN):
                    continue
                else:
                    functions.dict_entry_add(totals, entry, data[entry])

    # If this batch contains only deletes: Done
    if not totals:
        print('Skipped batch - no new entries.')
        return {'statusCode': 200}

    # Total Count of New Messages (for Printing)
    total_new_message_count = totals[constants.MESSAGE_COUNT_NAME]

    # Update all Values within one single transaction
    ddb_client = boto3.client('dynamodb', region_name=constants.REGION_NAME)

    # Batch of Items
    batch = [
        { 'Update':
            {
                'TableName' : constants.AGGREGATE_TABLE_NAME,
                'Key' : {constants.AGGREGATE_TABLE_KEY : {'S' : entry}},
                'UpdateExpression' : "ADD #val :val ",
                'ExpressionAttributeValues' : {
                    ':val': {'N' : str(totals[entry])}
                },
                'ExpressionAttributeNames': {
                    "#val" : "Value"
                }
            }
        } for entry in totals.keys()]

    # Calculate hash to ensure this batch hasn't been processed already:
    record_list_hash = hashlib.md5(str(records).encode()).hexdigest()

    response = ddb_client.transact_write_items(
        TransactItems = batch,
        ClientRequestToken = record_list_hash
    )

    # Manually Introduced Random Failure
    if random.uniform(0,100) < functions.get_parameter(ddb_ressource, "FAILURE_REDUCE_LAMBDA_PCT", 0):

        # Raise Exception
        raise Exception('Manually Introduced Random Failure!')

    # Print Status at End
    print('ReduceLambda finished. Updates aggregates with ' + str(total_new_message_count) + ' new message(s) in total.')

    return {'statusCode': 200}
```