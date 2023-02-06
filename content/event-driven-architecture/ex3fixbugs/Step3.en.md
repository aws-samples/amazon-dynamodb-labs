+++
title = "Optional: Add a simple Python frontend to view the data live"
date = 2019-12-02T10:45:32-08:00
weight = 3
+++

Congratulations, you succesfully completed *Lab 2*! If you've made it here and still have time left, we have added one optional step to the workshop for you! 

In this step, you will start an AWS Cloud9 instance and run a Python frontend that scans the DynamoDB `AggregateTable` twice per second and displays the results, i.e. the aggregated values for the different risk types, in your terminal.

![Architecture-1](/images/event-driven-architecture/lab2/lab2-optional.png)

{{% notice info %}}
AWS Cloud9 is by far not the only option to run this Python-based frontend! If you're motivated, feel free to try running it locally on your PC (make sure you run `aws configure` first - you can get your credentials on the EventEngine dashboard), or from any EC2 instance (e.g. assign an IAM role to the EC2 instance that allows access to the `AggregateTable`).
{{% /notice %}}

## Start an AWS Cloud9 instance
Since you're clearly experienced with AWS - making it through all of the lab - we'll leave this task up to you!

## Run the Python frontend
Once you're Cloud9 instance is running, make sure that the required Python library `boto3` is installed:

```python
pip3 install --user boto3
```

Now, you can copy the code below into a file, give it a descriptive name (e.g. `frontend.py`) and run it (`python3 frontend.py`). You should see the current aggregates from the `AggregationTable`, with new messages coming in every 60 seconds!

```python
# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

# --------------------------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------------------------

# General Imports
import time
import curses
import collections
from datetime import datetime

# AWS Imports
import boto3

# --------------------------------------------------------------------------------------------------
# Constants
# --------------------------------------------------------------------------------------------------

REGION_NAME                     = 'us-west-1'

AGGREGATE_TABLE_NAME            = 'AggregateTable'
AGGREGATE_TABLE_KEY             = 'Identifier'

MESSAGE_COUNT_NAME              = 'message_count'
VALUE_COLUMN_NAME               = 'Value'

# --------------------------------------------------------------------------------------------------
# Preparation
# --------------------------------------------------------------------------------------------------

# Connect to DynamoDB
ddb_ressource = boto3.resource('dynamodb', region_name=REGION_NAME)
table = ddb_ressource.Table(AGGREGATE_TABLE_NAME)

# Prepare Terminal
stdscr = curses.initscr()
curses.noecho()
curses.cbreak()

speed = None

# --------------------------------------------------------------------------------------------------
# Indefinite Loop - Pull Data and Print it to Console
# --------------------------------------------------------------------------------------------------

while True: 
    data = dict()
    message_count = 0

    # Read from DDB
    table_contents = table.scan(ConsistentRead = True)
    
    # Arrange for displaying
    if 'Items' in table_contents:
        for item in table_contents['Items']:
            identifier = item[AGGREGATE_TABLE_KEY]
            data[identifier] = item[VALUE_COLUMN_NAME]
                
    if data:
        message_count = data[MESSAGE_COUNT_NAME]
        del data[MESSAGE_COUNT_NAME]
        
        ordered_data = collections.OrderedDict(sorted(data.items()))
    
    # Init Speed
    if speed is None:
        speed_measure_start_time = time.time()
        speed_measure_start_count = message_count
        speed = 0
    
    # Update Speed
    time_now = time.time()
    time_diff = time_now - speed_measure_start_time
    if time_now - speed_measure_start_time > 5:
        speed = max(0, int(message_count - speed_measure_start_count) / time_diff)
        speed_measure_start_count = message_count
        speed_measure_start_time = time_now
    
    # Header
    stdscr.addstr(0 ,0, 'Current Time: ' + datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
    stdscr.addstr(1, 0, 'Total number of messages received: {}'.format(message_count))
    stdscr.addstr(2, 0, 'Current message influx: {:.1f} messages / second'.format(speed))

    # Data
    if message_count == 0:
        stdscr.addstr(4 ,0, 'No data to be displayed so far...')
    else:
        row = 4
        for k,v in ordered_data.items():
            if k[:10] == "timestamp_":
                continue
            level = k.count(':') 
            try:
                stdscr.addstr(row, 0, '{:<35}'.format(k) + (' ' * level) + '{:10.2f}'.format(v))
                row +=1
            except:
                pass
            
    stdscr.refresh()
    time.sleep(0.5)
    stdscr.clear()
```