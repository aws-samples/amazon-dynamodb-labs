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
    ddb_ressource = boto3.resource('dynamodb')

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
    ddb_client = boto3.client('dynamodb')

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

    response = ddb_client.transact_write_items(
        TransactItems = batch
    )

    # Manually Introduced Random Failure
    if random.uniform(0,100) < functions.get_parameter(ddb_ressource, "FAILURE_REDUCE_LAMBDA_PCT", 0):

        # Raise Exception
        raise Exception('Manually Introduced Random Failure!')

    # Print Status at End
    print('ReduceLambda finished. Updates aggregates with ' + str(total_new_message_count) + ' new message(s) in total.')

    return {'statusCode': 200}