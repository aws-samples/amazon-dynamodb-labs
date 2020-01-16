from __future__ import print_function
import boto3
import sys
import time
import threading
from multiprocessing import Queue
from lab_config import boto_args

queue = Queue()

def parallel_scan(tableName, totalsegments, threadsegment):
    dynamodb = boto3.resource(**boto_args)
    table = dynamodb.Table(tableName)

    totalbytessent = 0
    pageSize = 10000

    fe = "responsecode <> :f"
    eav = {":f": 200}

    response = table.scan(
        FilterExpression=fe,
        ExpressionAttributeValues=eav,
        Limit=pageSize,
        TotalSegments=totalsegments,
        Segment=threadsegment,
        ProjectionExpression='bytessent'
        )

    for i in response['Items']:
        totalbytessent += i['bytessent']

    while 'LastEvaluatedKey' in response:
        response = table.scan(
            FilterExpression=fe,
            ExpressionAttributeValues=eav,
            Limit=pageSize,
            TotalSegments=totalsegments,
            Segment=threadsegment,
            ExclusiveStartKey=response['LastEvaluatedKey'],
            ProjectionExpression='bytessent')
        for i in response['Items']:
            totalbytessent += i['bytessent']

    queue.put(totalbytessent)

if __name__ == "__main__":
    args = sys.argv[1:]
    tablename = args[0]
    total_segments = int(args[1])

    print('Scanning 1 million rows of table %s to get the total of bytes sent' %(tablename))

    begin_time = time.time()

    # BUGFIX https://github.com/boto/boto3/issues/1592
    boto3.resource(**boto_args)
    # 
    thread_list = []
    for i in range(total_segments):
        thread = threading.Thread(target=parallel_scan, args=(tablename, total_segments, i))
        thread.start()
        thread_list.append(thread)
        time.sleep(.1)

    for thread in thread_list:
        thread.join()

    totalbytessent = 0
    for i in range(total_segments):
        totalbytessent = totalbytessent + queue.get()

    print('Total bytessent %s in %s seconds' %(totalbytessent, time.time() - begin_time))
