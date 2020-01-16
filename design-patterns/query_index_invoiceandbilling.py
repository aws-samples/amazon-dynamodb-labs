from __future__ import print_function
import boto3
from boto3.dynamodb.conditions import Key, Attr
import time
import sys
import pprint
import os,pprint

def query_InvoiceandBilling(tablename,value):

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(tablename)

    if(value.startswith("I#")):
        print("\n =============================================================================================================== \n")
        print("!! No records found for {}. Pleaes use the query_invoiceandbilling.py for Invoice details.".format(value))
        print("\n =============================================================================================================== \n")
        exit()

    if(value.startswith("C#")):
        KCE = Key('SK').eq(value)
        response = table.query(IndexName='GSI_1',KeyConditionExpression=KCE)

    elif(value.startswith("B#")):
        KCE = Key('SK').eq(value)
        response = table.query(IndexName='GSI_1',KeyConditionExpression=KCE)
    return(response['Items'])

if __name__ == "__main__":
    os.system("clear")
    args = sys.argv[1:]
    tablename   =   args[0]
    value       =   args[1]

    begin_time = time.time()
    result = query_InvoiceandBilling(tablename,value)

    print("\n =============================================================================================================== \n")

    if(len(result)==0):
        print("\n!!!! No Records found for {} !!!!".format(value))

    if(len(result) > 0 and value.startswith("C#")):
        for i in result:
            if(len(i) == 2):
                print("\n Invoice ID: {}, Customer ID: {}\n".format(i['PK'],i['SK']))
            if(len(i) == 4):
                print("\n Customer ID: {}, Customer Name: {}, Location: {}".format(i['PK'],i['CustomerName'],i['State']))


    if(len(result) > 0 and value.startswith("B#")):
        for i in result:
            if(i['PK'].startswith("I#")):
                print("\n Invoice ID: {}, Bill ID: {}, BillAmount: {}, BillBalance: {}\n".format(i['PK'],i['SK'],i['BillAmount'],i['BillBalance']))
            if(i['PK'].startswith("B#")):
                print("\n Bill ID: {}, BillDueDate: {}\n".format(i['SK'],i['BillDueDate']))
    print("\n =============================================================================================================== \n")

    end_time = time.time()
    search_time = end_time-begin_time
    print("\n Results Retuned in : {}\n".format(search_time))
