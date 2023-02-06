# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

# --------------------------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------------------------

# General Imports
import random
import json
import base64
import hashlib
import time
import uuid
from decimal import Decimal

# AWS Imports
import boto3

# --------------------------------------------------------------------------------------------------
# AWS Settings
# --------------------------------------------------------------------------------------------------

# Kinesis
KINESIS_STREAM_NAME             = 'IncomingDataStream'

# DynamoDB Table and Column Names
PARAMETER_TABLE_NAME            = 'ParameterTable'
PARAMETER_TABLE_KEY             = 'parameter'
PARAMETER_COLUMN_NAME           = 'value'

AGGREGATE_TABLE_NAME            = 'AggregateTable'
AGGREGATE_TABLE_KEY             = 'Identifier'

MESSAGE_COUNT_NAME              = 'message_count'

ID_COLUMN_NAME                  = 'TradeID'
VERSION_COLUMN_NAME             = 'Version'
VALUE_COLUMN_NAME               = 'Value'
TIMESTAMP_COLUMN_NAME           = 'Timestamp'
HIERARCHY_COLUMN_NAME           = 'Hierarchy'

HIERARCHY_DEFINITION            =  {
                                    'RiskType'  : ['PV', 'Delta'],
                                    'Region'    : ['EMEA', 'APAC', 'AMER'],
                                    'TradeDesk' : ['FXSpot', 'FXOptions']
                                }

TIMESTAMP_GENERATOR_FIRST       = 'timestamp_generator_first'
TIMESTAMP_GENERATOR_MEAN        = 'timestamp_generator_mean'
   
# --------------------------------------------------------------------------------------------------
# Aggregation Settings
# --------------------------------------------------------------------------------------------------

# Definition of the Hierarchy
AGGREGATION_HIERARCHY = ['RiskType', 'TradeDesk', 'Region']

# --------------------------------------------------------------------------------------------------
# Generator Settings
# --------------------------------------------------------------------------------------------------

# Number of messages per Generator
NUMBER_OF_BATCHES                   = 250
BATCH_SIZE                          = 40

# Risk Values
MIN_VALUE_OF_RISK                   = 0
MAX_VALUE_OF_RISK                   = 100000

# Other
TIME_INTERVAL_SPEED_CALCULATION     = 3

# Lambda Settings
FAILURE_STATE_LAMBDA_PCT            = 5
FAILURE_MAP_LAMBDA_PCT              = 10
FAILURE_REDUCE_LAMBDA_PCT           = 10

# --------------------------------------------------------------------------------------------------
# Generic Helper Functions
# --------------------------------------------------------------------------------------------------

# Add a value to an entry in a dictionary, create the entry if necessary
def dict_entry_add(dictionary, key, value):
    if key in dictionary:
        dictionary[key] += value
    else:
        dictionary[key] = value
        
# Add a value to an entry in a dictionary, create the entry if necessary
def dict_entry_min(dictionary, key, value):
    if (key not in dictionary) or (value < dictionary[key]):
        dictionary[key] = value

# --------------------------------------------------------------------------------------------------
# AWS Helper Functions
# --------------------------------------------------------------------------------------------------

# Get item from a DynamoDB Table, if it exists, return None otherwise
def get_item_ddb(table, key_name, strong_consistency = False):
    
    # Call to DynamoDB
    if strong_consistency:
        response = table.get_item(Key=key_name,ConsistentRead = True)
    else:
        response = table.get_item(Key=key_name)
    
    # Return item if found
    if 'Item' in response:
        item = response['Item']
    else:
        item = None
   
    return item

# Count number of items in DynamoDB Table
def count_items(table):
    
    item_count = 0
    scan_args = dict()
    done = False
    start_key = None
    i = 0
    
    while not done:
        # Scan
        if start_key:
            scan_args['ExclusiveStartKey'] = start_key
        response = table.scan(**scan_args)
        start_key = response.get('LastEvaluatedKey', None)
        done = start_key is None
    
        # Get Items
        items = response.get('Items', [])
        item_count += len(items)
    
    return item_count

# Get Parameter Value
def get_parameter(ddb_ressource, param_name, default_val):
    parameter_table = ddb_ressource.Table(PARAMETER_TABLE_NAME)
    response = get_item_ddb(parameter_table, {PARAMETER_TABLE_KEY : param_name}, True)
    
    if response:
        return int(response[PARAMETER_COLUMN_NAME])
    else:
        return default_val
    
# Set Parameter Value
def set_parameter(ddb_ressource, param_name, param_val):
    parameter_table = ddb_ressource.Table(PARAMETER_TABLE_NAME)
    response = parameter_table.put_item(Item = {
        PARAMETER_TABLE_KEY : param_name,
        PARAMETER_COLUMN_NAME : Decimal(str(param_val))
        })
    return response

# --------------------------------------------------------------------------------------------------
# Aggregation & Generator Helper Functions
# --------------------------------------------------------------------------------------------------

# Random Value
def random_value():
    value = random.randint(100 * MIN_VALUE_OF_RISK, 100 * MAX_VALUE_OF_RISK) / 100
    return value

# Random Type Constructor
def random_hierarchy():
    hierarchy = dict()
    for k,v in HIERARCHY_DEFINITION.items():
        hierarchy[k] = random.choice(v)
    return hierarchy

# Convert a Hierarchy Dictionary to a Type String, based on Aggregation Hierarchy
def hierarchy_to_string (hierarchy_dictionary, aggregation_hierarchy):
    type_string = ''
    start = True
    for level in aggregation_hierarchy:
        if start:
            start = False
        else:
            type_string += ":"
            
        type_string += hierarchy_dictionary[level]
    return type_string

# Aggregate along tree
def aggregate_along_tree(data):
    
    # Determine aggregation depth
    aggregation_depth = max([key.count(':') for key in data.keys()])

    # Start at max depth and go higher 
    for depth in range(aggregation_depth, 0, -1):
        children = [key for key in data.keys() if key.count(':') == depth]
        for child in children:
            parent = child[:child.rfind(':')]
            dict_entry_add(data, parent, data[child])
                
    return data

# Aggregate over records from a DynamoDB Stream (Stateful Pipeline)
def aggregate_over_dynamo_records(records):

    # Initialize Delta Dict
    delta = dict()

     # Iterate over Messages
    for record in records:

        # If the record doesn't contain new data: Skip
        if 'NewImage' not in record['dynamodb']:
            continue

        # Add New Image to Aggregate
        new_data = record['dynamodb']['NewImage']

        new_hierarchy       = json.loads(   new_data[HIERARCHY_COLUMN_NAME]['S'] )
        new_value           = float(        new_data[VALUE_COLUMN_NAME]['N']     )
        new_generated_time  = float(        new_data[TIMESTAMP_COLUMN_NAME]['N'] )
        
        # Add to Value for the New Type
        new_type = hierarchy_to_string(new_hierarchy, AGGREGATION_HIERARCHY)
        dict_entry_add(delta, new_type, new_value)
        
        # Times
        dict_entry_add(delta, TIMESTAMP_GENERATOR_MEAN, new_generated_time)
        dict_entry_min(delta, TIMESTAMP_GENERATOR_FIRST, new_generated_time)
            
        # If the record contains old data: Delete from Aggregate
        if 'OldImage' in record['dynamodb']:
            old_data = record['dynamodb']['OldImage']

            old_hierarchy   = json.loads(   old_data[HIERARCHY_COLUMN_NAME]['S'] )
            old_value       = float(        old_data[VALUE_COLUMN_NAME]['N']     )

            # Subtract from Value for the Old Type
            old_type = hierarchy_to_string(old_hierarchy, AGGREGATION_HIERARCHY)
            dict_entry_add(delta, old_type, - old_value)

        # Increment mesage count
        dict_entry_add(delta, MESSAGE_COUNT_NAME, 1)
        
    # Adjust timestamp mean by number of messages
    if delta:
        delta[TIMESTAMP_GENERATOR_MEAN] /= delta[MESSAGE_COUNT_NAME]

    return delta

# Aggregate over records from a Kinesis Stream (Stateless Pipeline)
def aggregate_over_kinesis_records(records):

    # Initialize Delta Dict
    delta = dict()

     # Iterate over Messages
    for record in records:

        data = json.loads(base64.b64decode(record['kinesis']['data']).decode('utf-8'))

        # Get Relevant Data
        record_hierarchy    = data[HIERARCHY_COLUMN_NAME]
        record_value        = data[VALUE_COLUMN_NAME]
        record_time         = data[TIMESTAMP_COLUMN_NAME]
        
        # Add to Value for the New Type
        record_type = hierarchy_to_string(record_hierarchy, AGGREGATION_HIERARCHY)
        dict_entry_add(delta, record_type, record_value)
        
        # Times
        dict_entry_add(delta, TIMESTAMP_GENERATOR_MEAN, record_time)
        dict_entry_min(delta, TIMESTAMP_GENERATOR_FIRST, record_time)
            
        # Increment mesage count
        dict_entry_add(delta, MESSAGE_COUNT_NAME, 1)
        
    # Adjust timestamp mean by number of messages
    if delta:
        delta[TIMESTAMP_GENERATOR_MEAN] /= delta[MESSAGE_COUNT_NAME]

    return delta


# --------------------------------------------------------------------------------------------------
# Generate Messages
# --------------------------------------------------------------------------------------------------

def generate_messages(SPECIAL_TRADES):
    
    if SPECIAL_TRADES:
        DUPLICATES_PER_BATCH            = 5
        PERCENTAGE_MODIFY               = 3
        PERCENTAGE_OUT_OR_ORDER         = 100
    else:
        DUPLICATES_PER_BATCH                = 0
        PERCENTAGE_MODIFY                   = 0
        PERCENTAGE_OUT_OR_ORDER             = 0

    state = dict()
    totals = dict()
    
    for i in range(NUMBER_OF_BATCHES):
    
        # Initialize record list for this batch
        records = []
        
        # Calculate number of duplicates that are added at the end
        if DUPLICATES_PER_BATCH < BATCH_SIZE:
            number_of_duplicate_messages = DUPLICATES_PER_BATCH
        else:
            number_of_duplicate_messages = max(0, BATCH_SIZE - 1)
        
        # Create Batch
        for j in range(BATCH_SIZE - number_of_duplicate_messages):
            
            # Initialize Empty Message
            message = {}
            
            # Random decision: Modify or New Entry
            if len(state) == 0 or \
                random.uniform(0,100) < (100 - PERCENTAGE_MODIFY):

                # -> New Entry

                # Generate ID
                message[ID_COLUMN_NAME] = str(uuid.uuid4())
                
                # Add Version
                message[VERSION_COLUMN_NAME] = 0
                
                # Count
                dict_entry_add(totals, 'count:add', 1)
                
            else:

                # -> Modify

                # Pick existing ID
                message[ID_COLUMN_NAME] = random.choice(list(state.keys()))
                
                # Get New Version
                if state[message[ID_COLUMN_NAME]][VERSION_COLUMN_NAME] == 0 or \
                    random.uniform(1,100) < (100 - PERCENTAGE_OUT_OR_ORDER):
                    # Iterate Version
                    message[VERSION_COLUMN_NAME] = \
                        state[message[ID_COLUMN_NAME]][VERSION_COLUMN_NAME] + 1
                    dict_entry_add(totals, 'count:modify:in_order', 1)
                else:
                    # Insert Older Version
                    message[VERSION_COLUMN_NAME] = \
                        state[message[ID_COLUMN_NAME]][VERSION_COLUMN_NAME] - 1
                    dict_entry_add(totals, 'count:modify:out_of_order', 1)
                
            # Add Random Value 
            message[VALUE_COLUMN_NAME] = random_value()
            
            # Add Random Hierarchy
            message[HIERARCHY_COLUMN_NAME] = random_hierarchy()
            
            # Add Timestamp
            message[TIMESTAMP_COLUMN_NAME] = time.time()
            
            # Dump to String
            message_string = json.dumps(message)
            
            # Append to Record List
            record = {'Data' : message_string, 'PartitionKey' : 
                hashlib.sha256(message_string.encode()).hexdigest()}
            records.append(record)
            
            # Append to Internal Storage - if message was sent in order
            if (message[ID_COLUMN_NAME] not in state) or \
                (state[message[ID_COLUMN_NAME]][VERSION_COLUMN_NAME] \
                < message[VERSION_COLUMN_NAME]):
                state[message[ID_COLUMN_NAME]] = message
    
        # Add Duplicates
        for k in range(number_of_duplicate_messages):
            duplicate_index = random.randint(0, BATCH_SIZE - number_of_duplicate_messages - 1)
            records.append(records[duplicate_index])
        
        dict_entry_add(totals, 'count:duplicates', number_of_duplicate_messages)

        # Send Batch to Kinesis Stream
        response = kinesis_client.put_records(StreamName=KINESIS_STREAM_NAME,Records=records)

    # Aggregate over Final State
    for entry in state.values():
        k = hierarchy_to_string(entry[HIERARCHY_COLUMN_NAME], AGGREGATION_HIERARCHY)
        v = entry[VALUE_COLUMN_NAME]
        dict_entry_add(totals, k, v)

    return totals

# --------------------------------------------------------------------------------------------------
# Preparation
# --------------------------------------------------------------------------------------------------

# Connect to DynamoDB
ddb_ressource = boto3.resource('dynamodb')
aggregate_table = ddb_ressource.Table(AGGREGATE_TABLE_NAME)
    
# Initialize Kinesis Consumer
kinesis_client = boto3.client('kinesis')

def lambda_handler(event, context):

    print("New Batch.")

    # --------------------------------------------------------------------------------------------------
    # Get current values from aggregate tables
    # --------------------------------------------------------------------------------------------------

    # Init data structure
    data_before_ingestion = dict()

    # Read from DDB
    table_contents = aggregate_table.scan(ConsistentRead = True)
    
    if 'Items' in table_contents:
        for item in table_contents['Items']:
            identifier = item[AGGREGATE_TABLE_KEY]
            data_before_ingestion[identifier] = item[VALUE_COLUMN_NAME]
    
    print("Read current aggregates.")
    
    # --------------------------------------------------------------------------------------------------
    # Generate new Data
    # --------------------------------------------------------------------------------------------------
    
    # Special Trades?
    SPECIAL_TRADES = bool(get_parameter(ddb_ressource, "SPECIAL_TRADES", 0))

    totals = generate_messages(SPECIAL_TRADES)
    print("Ingested " + str(NUMBER_OF_BATCHES * BATCH_SIZE) + " messages into pipeline.")

    # --------------------------------------------------------------------------------------------------
    # Check Totals against results of the participants
    # --------------------------------------------------------------------------------------------------

    # Wait for 30 seconds - allow pipelines to aggregate & process
    time.sleep(30)

    # Init data structure
    data_after_ingestion = dict()

    # Read from DDB
    table_contents = aggregate_table.scan(ConsistentRead = True)
    
    # Arrange for displaying
    if 'Items' in table_contents:
        for item in table_contents['Items']:
            identifier = item[AGGREGATE_TABLE_KEY]
            data_after_ingestion[identifier] = item[VALUE_COLUMN_NAME]
            
            # Subtract value from before
            if identifier in data_before_ingestion:
                data_after_ingestion[identifier] -= data_before_ingestion[identifier]
    print("Read new aggregates.")

    # Get Generated Totals
    totals = aggregate_along_tree(totals)

    # Evaluation
    score = 100
    for risk in totals:
        if (risk[:5] != "count") and ((risk not in data_after_ingestion) or (abs(totals[risk] - float(data_after_ingestion[risk])) > 1.e-5)):
            score = 0
            break
    
    # Update Score Table
    current_score = get_parameter(ddb_ressource, "SCORE", 0)
    total_score = round(score + current_score,0)
    set_parameter(ddb_ressource, "SCORE", total_score)

    print("Scoring completed. Score for this batch: " + str(round(score,0)) + ". Total score: " + str(total_score) + ".")

    # Move to Lab 2
    if(total_score >= 300):
        
        # Activate Special Trades
        set_parameter(ddb_ressource, "SPECIAL_TRADES", 1)

        # Start Manual Failing of Lambdas
        set_parameter(ddb_ressource, "FAILURE_STATE_LAMBDA_PCT",    FAILURE_STATE_LAMBDA_PCT)
        set_parameter(ddb_ressource, "FAILURE_MAP_LAMBDA_PCT",      FAILURE_MAP_LAMBDA_PCT)
        set_parameter(ddb_ressource, "FAILURE_REDUCE_LAMBDA_PCT",   FAILURE_REDUCE_LAMBDA_PCT)

    return {'statusCode': 200}