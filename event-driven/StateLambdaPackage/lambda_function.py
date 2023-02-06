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
        table.update_item(
            Key = {
                constants.STATE_TABLE_KEY: record_id
                },
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

    # Print Status at End
    print('StateLambda successfully processed ' + str(len(records)) + ' record(s).')

    return {'statusCode': 200}