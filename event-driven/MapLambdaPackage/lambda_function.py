# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

# --------------------------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------------------------

# General Imports
import json
import hashlib
import random

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
    print('Invoked MapLambda with ' + str(len(records)) + ' record(s).')

    # Aggregate incoming messages (only over the leafs)
    delta = functions.aggregate_over_dynamo_records(records)
    
    # If the batch contains only deletes: Done.
    if not delta:
        print('Skipped batch - no new entries.')
        return {'statusCode': 200}

    # Aggregate along the tree
    delta = functions.aggregate_along_tree(delta)

    # Create Message
    message = json.dumps(delta, sort_keys = True)
    
    # Compute hash over all records
    message_hash = hashlib.sha256(str(records).encode()).hexdigest()

    # Write to DynamoDB
    ddb_ressource = boto3.resource('dynamodb')
    table = ddb_ressource.Table(constants.DELTA_TABLE_NAME)

    # We use a conditional put based on the hash of the record list to ensure
    # we're not accidentally writing one batch twice.
    try: 
        table.put_item(
            Item={
                'MessageId': message_hash,
                'Message': message
                },
            ConditionExpression='attribute_not_exists(MessageId)'
            )
    except ClientError as e:
        if e.response['Error']['Code']=='ConditionalCheckFailedException':   
            print('Conditional Put failed. Item with MessageId ' + message_hash + \
                ' already exists.')
            print('Item:', message)
            print('Full Exception: ' + str(e) + '.')
        else:
            print(e)
            return {'statusCode': 500}
    
    # Manually Introduced Random Failure
    if random.uniform(0,100) < functions.get_parameter(ddb_ressource, "FAILURE_MAP_LAMBDA_PCT", 0):
        
        # Raise exception
        raise Exception('Manually Introduced Random Failure!')

    print('MapLambda finished. Aggregated ' + str(delta[constants.MESSAGE_COUNT_NAME]) + \
        ' message(s) and written to DeltaTable. MessageHash: ' + message_hash + '.')
   
    return {'statusCode': 200}
