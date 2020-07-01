from __future__ import print_function
import boto3
from boto3.dynamodb.conditions import Key, Attr
import time
import sys
from lab_config import boto_args

def query_gsi(tableName,attribute,value,):
    dynamodb = boto3.resource(**boto_args)
    table = dynamodb.Table(tableName)

    if attribute == 'name':
        ke = Key('GSI_1_PK').eq('root') & Key('GSI_1_SK').eq(value)
    else:
        ke = Key('GSI_1_PK').eq(attribute + "#" + value)

    response = table.query(
        IndexName='GSI_1',
        KeyConditionExpression=ke
        )

    print('List of employees with %s in the attribute %s:' % (value,attribute))
    for i in response['Items']:
        print('\tEmployee name: %s - hire date: %s' % (i['name'],i['hire_date']))

    return response['Count']

if __name__ == "__main__":
    args = sys.argv[1:]
    tableName = args[0]
    attribute = args[1]
    value = args[2]

    begin_time = time.time()
    count = query_gsi(tableName,attribute,value)
    print ('Total of employees: %s. Execution time: %s seconds' % (count, time.time() - begin_time))
#
