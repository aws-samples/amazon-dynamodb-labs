from __future__ import print_function # Python 2/3 compatibility
import boto3
import time
import csv
import sys
from lab_config import boto_args


def import_csv(tableName, fileName, attributesNameList, attributesTypeList):
    dynamodb = boto3.resource(**boto_args)
    dynamodb_table = dynamodb.Table(tableName)
    count = 0

    servererror = False
    time1 = time.time()
    with open(fileName, 'r', encoding="utf-8") as csvfile:
        myreader = csv.reader(csvfile, delimiter=',')
        for row in myreader:
            count += 1
            newitem = {}
            for colunm_number, colunm_name in enumerate(attributesNameList):
                newitem[colunm_name] = attributesTypeList[colunm_number](row[colunm_number])
            # Create primary keys
            newitem["PK"] = "request#{}".format(newitem['requestid'])
            newitem["GSI_1_PK"] = "host#{}".format(newitem['host'])

            if newitem['responsecode'] == 500:
                newitem['servererror'] = '5xx'

            item = dynamodb_table.put_item(Item=newitem)

            if count % 100 == 0:
                time2 = time.time() - time1
                print("row: %s in %s" % (count, time2))
                time1 = time.time()
    return count

if __name__ == "__main__":
    args = sys.argv[1:]
    tableName = args[0]
    fileName = args[1]

    attributesNameList = ['requestid','host','date','hourofday','timezone','method','url','responsecode','bytessent','useragent']
    attributesTypeList = [int,str,str,int,str,str,str,int,int,str]

    begin_time = time.time()
    count = import_csv(tableName, fileName, attributesNameList, attributesTypeList)

    # print summary
    print('RowCount: %s, Total seconds: %s' %(count, (time.time() - begin_time)))
