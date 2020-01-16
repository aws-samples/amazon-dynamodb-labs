from __future__ import print_function
import boto3
import time
import sys
from lab_config import boto_args

def scan_table(tableName):
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
        ProjectionExpression='bytessent')

    for i in response['Items']:
        totalbytessent += i['bytessent']

    while 'LastEvaluatedKey' in response:
        response = table.scan(
            FilterExpression=fe,
            ExpressionAttributeValues=eav,
            Limit=pageSize,
            ExclusiveStartKey=response['LastEvaluatedKey'],
            ProjectionExpression='bytessent')
        for i in response['Items']:
            totalbytessent += i['bytessent']
    return totalbytessent

if __name__ == "__main__":
    args = sys.argv[1:]
    tablename = args[0]

    print('Scanning 1 million rows of table %s to get the total of bytes sent' %(tablename))

    begin_time = time.time()

    totalbytessent = scan_table(tablename)

    print ('Total bytessent %s in %s seconds' % (totalbytessent, time.time() - begin_time))
