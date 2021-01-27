from __future__ import print_function # Python 2/3 compatibility
import boto3
import time
from boto3.dynamodb.conditions import Key, Attr
import csv
import sys
from lab_config import boto_args

def import_csv(tableName, fileName):
    dynamodb = boto3.resource(**boto_args)
    west_table = dynamodb.Table(tableName)
    count = 0

    time1 = time.time()
    with open(fileName, 'r', encoding="utf-8") as csvfile:
        myreader = csv.reader(csvfile, delimiter=',')
        for row in myreader:
            count += 1
            newRecommendation = {}
            #primary keys
            newRecommendation['customer_id'] = row[0]
            newRecommendation['category_id'] = row[1]
            newRecommendation['title'] = row[2]

            newRecommendation['region'] = 'West'
            item = west_table.put_item(Item=newRecommendation)

            response = west_table.query(
            KeyConditionExpression=Key('customer_id').eq(row[0]) & Key('category_id').eq(row[1])
            )

            print(response['Items'])
            print("Current time: %s" % time.time())

            time.sleep(1)

            response = west_table.query(
            KeyConditionExpression=Key('customer_id').eq(row[0]) & Key('category_id').eq(row[1])
            )

            print(response['Items'])
            print("Current time: %s\n" % time.time())

            if count % 100 == 0:
                time2 = time.time() - time1
                print("recommendations count: %s in %s" % (count, time2))
                time1 = time.time()
    return count

if __name__ == "__main__":
    args = sys.argv[1:]
    tableName = args[0]
    fileName = args[1]

    begin_time = time.time()
    count = import_csv(tableName, fileName)

    # print summary
    print('RowCount: %s, Total seconds: %s' %(count, (time.time() - begin_time)))
