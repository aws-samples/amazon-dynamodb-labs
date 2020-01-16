
from __future__ import print_function
import boto3
from boto3.dynamodb.conditions import Key, Attr
import time
import sys
import argparse
import threading
from multiprocessing import Queue
from lab_config import boto_args

queue = Queue()

def query_responsecode_shard(tableName, shardid, responsecode, date="all"):
    dynamodb = boto3.resource(**boto_args)
    table = dynamodb.Table(tableName)

    if date == "all":
        ke = Key('GSI_1_PK').eq("shard#{}".format(shardid)) & Key('GSI_1_SK').begins_with(responsecode)
    else:
        ke = Key('GSI_1_PK').eq("shard#{}".format(shardid)) & Key('GSI_1_SK').begins_with(responsecode+"#"+date)

    response = table.query(
        IndexName='GSI_1',
        KeyConditionExpression=ke
        )

    print('Records with response code %s in the shardid %s = %s' %(responsecode, shardid, response['Count']))
    queue.put(response['Count'])

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("table", help="table name")
    parser.add_argument("responsecode", help="response code [200, 304, 404, 500]")
    parser.add_argument("--date", help="date ['2017-07-20','2017-07-21','2017-07-22']", default="all")
    args = parser.parse_args()

    SHARDS = 10

    begin_time = time.time()
    thread_list = []
    # BUGFIX https://github.com/boto/boto3/issues/1592
    boto3.resource(**boto_args)
    #
    for i in range(SHARDS):
        thread = threading.Thread(target=query_responsecode_shard, args=(args.table, i, args.responsecode, args.date))
        thread.start()
        thread_list.append(thread)
        time.sleep(.1)

    for thread in thread_list:
        thread.join()

    count = 0
    for i in range(SHARDS):
        count = count + queue.get()

    print('Number of records with responsecode %s is %s. Query time: %s seconds' %(args.responsecode, count, time.time() - begin_time))
