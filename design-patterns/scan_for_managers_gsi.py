from __future__ import print_function
import boto3
import time
import sys
from lab_config import boto_args

def scan_table(tableName,pageSize):
    dynamodb = boto3.resource(**boto_args)
    table = dynamodb.Table(tableName)

    page = 1
    count = 0
    managers_count = 0

    response = table.scan(
        Limit=pageSize,
        IndexName='GSI_2'
        )

    count = count + response['ScannedCount']
    managers_count = managers_count + response['Count']

    while 'LastEvaluatedKey' in response:
        page += 1
        response = table.scan(
            Limit=pageSize,
            IndexName='GSI_2',
            ExclusiveStartKey=response['LastEvaluatedKey'])
        count = count + response['ScannedCount']
        managers_count = managers_count + response['Count']

    return count, managers_count

if __name__ == "__main__":
    args = sys.argv[1:]
    tableName = args[0]
    pagesize = args[1]

    begin_time = time.time()
    count, managers_count = scan_table(tableName,int(pagesize))

    print ('Number of managers: %s. # of records scanned: %s. Execution time: %s seconds' % (managers_count, count, time.time() - begin_time))
