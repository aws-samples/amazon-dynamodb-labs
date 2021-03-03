from __future__ import print_function
import boto3
from boto3.dynamodb.conditions import Key, Attr
import time
import sys
import argparse
from lab_config import boto_args

def query_gsi(tableName, value1, value2):
    dynamodb = boto3.resource(**boto_args)
    table = dynamodb.Table(tableName)

    if value2 == "-":
        ke = Key('GSI_3_PK').eq("state#{}".format(value1))
    else:
        ke = Key('GSI_3_PK').eq("state#{}".format(value1)) & Key('GSI_3_SK').begins_with(value2)

    response = table.query(
        IndexName='GSI_3',
        KeyConditionExpression=ke
        )

    print('List of employees . State: %s' % (value1))

    for i in response['Items']:
        city,dept = i['city_dept'].split('#')
        print('\tName: %s. City: %s. Dept: %s' % (i['name'], city, dept))

    return response['Count']

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("table", help="table name")
    parser.add_argument("state", help="state name")
    parser.add_argument("--citydept", help="begin of city and dept in the format city#dept, examples, Sea or Seattle#Dev")
    args = parser.parse_args()

    tableName = args.table
    value1 = args.state
    if args.citydept:
        value2 = args.citydept
    else:
        value2 = "-"

    begin_time = time.time()
    count = query_gsi(tableName, value1, value2)
    print ('Total of employees: %s. Execution time: %s seconds' % (count, time.time() - begin_time))
#
