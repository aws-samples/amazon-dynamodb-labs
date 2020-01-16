from __future__ import print_function
import boto3
import botocore
import sys
import decimal
import time
from lab_config import boto_args
# TODO this is unused
def update_employee(tableName, employeeid, newstate, newcity, newdept):
    dynamodb = boto3.resource(**boto_args)
    table = dynamodb.Table(tableName)

    masterUpdateSuccess = 'True'
    try:
        # setting the lock attribute to 1, locking the employee item
        # updating the location to the new value
        masterresponse = table.update_item(
            Key={'employeeid': decimal.Decimal(employeeid), 'colA': 'master'},
            UpdateExpression="set #a = :v1, #b = :v2, #c = :v3, #l = :l1",
            ConditionExpression="#l = :l0",
            ExpressionAttributeNames={'#a': 'state', '#b': 'city', '#c': 'city_dept', '#l': 'lock'},
            ExpressionAttributeValues={':v1': newstate, ':v2': newcity, ':v3': newcity+":"+newdept, ':l1': '1', ':l0' : '0'},
            ReturnValues="ALL_OLD"
        )

        oldstate = masterresponse['Attributes']['state']
        oldcity = masterresponse['Attributes']['city']
        oldhire_date = masterresponse['Attributes']['hire_date']
        oldname = masterresponse['Attributes']['name']

        print('Updating the items related to the employee %s' % (oldname))
        print('Please wait 60 seconds')

    except botocore.exceptions.ClientError as e:
        # employee item was locked, returning ConditionalCheckFailedException
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            masterUpdateSuccess = 'False'

    # update the location item for the same employee employeeid, if the lock was acquired
    if masterUpdateSuccess == 'True':
        # it is not possible to change the sort key value
        # you need to delete the existing item and add a new one with the new location
        response = table.delete_item(
            Key={'employeeid': decimal.Decimal(employeeid), 'colA': 'state:' + oldstate},
        )

        response = table.put_item(
            Item={
                'employeeid': decimal.Decimal(employeeid),
                'colA': 'state:' + newstate,
                'hire_date': oldhire_date,
                'name': oldname
            }
        )

        # adding a wait time before release the item
        time.sleep(60)

        # setting the lock attribute to 0, releasing the item
        masterresponse = table.update_item(
            Key={'employeeid': decimal.Decimal(employeeid), 'colA': 'master'},
            UpdateExpression="set #l = :l0",
            ConditionExpression="#l = :l1",
            ExpressionAttributeNames={'#l': 'lock'},
            ExpressionAttributeValues={':l1': '1', ':l0' : '0'},
            ReturnValues="ALL_OLD"
        )

    # print(masterUpdateSuccess)

    return masterUpdateSuccess

if __name__ == "__main__":
    args = sys.argv[1:]
    tableName = args[0]
    employeeid = args[1]
    newstate = args[2]
    newcity = args[3]
    newdept = args[4]

    ret = update_employee(tableName, employeeid, newstate, newcity, newdept)

    if ret == 'True':
        print ('\tEmployee: %s updated to %s / %s.' % (employeeid, newcity, newstate))
    else:
        print ('\tEmployee: %s cannot be updated. Employee locked. ' % (employeeid))
