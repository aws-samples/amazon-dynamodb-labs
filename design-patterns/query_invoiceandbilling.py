from __future__ import print_function
import boto3
from boto3.dynamodb.conditions import Key, Attr
import time
import sys
import pprint
import os

def query_InvoiceandBilling(tablename,value):

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(tablename)

    if(value.startswith("I#")):
        KCE = Key('PK').eq(value)
        response = table.query(KeyConditionExpression=KCE)
        return(response['Items'])

    if(value.startswith("B#") or value.startswith("C#")):
        print("\n ============================================================================================================================== \n")
        print("\n No records found for {}. Please use the query_index_invoiceandbilling.py script for querying Customer and Billing details.\n".format(value))
        print("\n ============================================================================================================================== \n")
        exit()

if __name__ == "__main__":
    os.system("clear")
    args = sys.argv[1:]
    tablename   =   args[0]
    value       =   args[1]

    begin_time = time.time()
    result = query_InvoiceandBilling(tablename,value)

    print("\n ============================================================================================================================== \n")
    if(len(result)==0):
        print("\n!!!! No Records found for {}. !!!!".format(value))

    if(len(result) > 0 and value.startswith("I#")):
        for i in result:
            if(len(i) == 4):
                print("\n Invoice ID:{}, BillID:{}, BillAmount:{}, BillBalance:{}".format(i['PK'],i['SK'],i['BillAmount'],i['BillBalance']))
            if(len(i) == 6):
                print("\n Invoice ID:{}, InvoiceStatus:{}, InvoiceBalance:{}, InvoiceDate:{}, InvoiceDueDate:{}".format(i['PK'],i['InvoiceStatus'],i['InvoiceBalance'],i['InvoiceDate'],i['InvoiceDueDate']))
            if(len(i) == 2):
                print("\n Invoice ID:{}, Customer ID:{}".format(i['PK'],i['SK']))

    print("\n ============================================================================================================================== \n")

    end_time = time.time()
    search_time = end_time-begin_time
    print("\n Results Retuned in : {}\n".format(search_time))
