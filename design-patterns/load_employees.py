from __future__ import print_function # Python 2/3 compatibility
import boto3
import time
import csv
import sys
from lab_config import boto_args

def import_csv(tableName, fileName):
    dynamodb = boto3.resource(**boto_args)
    dynamodb_table = dynamodb.Table(tableName)
    count = 0

    time1 = time.time()
    with open(fileName, 'r', encoding="utf-8") as csvfile:
        myreader = csv.reader(csvfile, delimiter=',')
        for row in myreader:
            count += 1
            newEmployee = {}
            #primary keys
            newEmployee['PK'] = "e#{}".format(row[0])
            newEmployee['SK']  = 'root'
            newEmployee['GSI_1_PK'] = 'root'
            newEmployee['GSI_1_SK']  = row[1]
            newEmployee['GSI_3_PK'] = "state#{}".format(row[5])
            newEmployee['GSI_3_SK'] = "{}#{}".format(row[4], row[3])

            newEmployee['employeeid'] = int(row[0])
            newEmployee['name'] = row[1]
            newEmployee['title'] = row[2]
            newEmployee['dept'] = row[3]
            newEmployee['city'] = row[4]
            newEmployee['state'] = row[5]
            newEmployee['city_dept'] = newEmployee['GSI_3_SK']
            newEmployee['dob'] = row[6]
            newEmployee['hire_date'] = row[7]
            newEmployee['previous_title'] = row[8]
            newEmployee['previous_title_end'] = row[9]
            newEmployee['lock']  = '0'
            if len(row) == 11:
                newEmployee['is_manager'] = row[10]
                newEmployee['GSI_2_PK'] = str(newEmployee['is_manager'])
                newEmployee['GSI_2_SK'] = "root"


            item = dynamodb_table.put_item(Item=newEmployee)

            newCurrentTitle = {}
            newCurrentTitle['employeeid'] = newEmployee['employeeid']
            newCurrentTitle['name'] = newEmployee['name']
            newCurrentTitle['hire_date'] = newEmployee['hire_date']
            newCurrentTitle['PK'] = newEmployee['PK']
            newCurrentTitle['SK'] = 'current_title#' + newEmployee['title']
            newCurrentTitle['GSI_1_PK'] = newCurrentTitle['SK']
            newCurrentTitle['GSI_1_SK'] = newCurrentTitle['name']
            item = dynamodb_table.put_item(Item=newCurrentTitle)

            newPreviousTitle = {}
            newPreviousTitle['employeeid'] = newEmployee['employeeid']
            newPreviousTitle['name'] = newEmployee['name']
            newPreviousTitle['hire_date'] = newEmployee['hire_date']
            newPreviousTitle['PK'] = newEmployee['PK']
            newPreviousTitle['SK'] = 'previous_title#' + newEmployee['previous_title']
            newPreviousTitle['GSI_1_PK'] = newPreviousTitle['SK']
            newPreviousTitle['GSI_1_SK'] = newPreviousTitle['name']
            item = dynamodb_table.put_item(Item=newPreviousTitle)

            newLocation = {}
            newLocation['employeeid'] = newEmployee['employeeid']
            newLocation['name'] = newEmployee['name']
            newLocation['hire_date'] = newEmployee['hire_date']
            newLocation['city_dept'] = newEmployee['city_dept']
            newLocation['PK'] = newEmployee['PK']
            newLocation['SK'] = 'state#' + newEmployee['state']
            newLocation['GSI_1_PK'] = newLocation['SK']
            newLocation['GSI_1_SK'] = newLocation['name']

            item = dynamodb_table.put_item(Item=newLocation)

            if count % 100 == 0:
                time2 = time.time() - time1
                print("employee count: %s in %s" % (count, time2))
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
