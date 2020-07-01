from __future__ import print_function # Python 2/3 compatibility
import boto3
import time
import csv
import sys

def import_csv(tableName, fileName):
  dynamodb = boto3.resource('dynamodb')
  dynamodb_table = dynamodb.Table(tableName)
  count = 0

  time1 = time.time()
  with open(fileName, 'r', encoding="utf-8") as csvfile:
    myreader = csv.reader(csvfile, delimiter=',')
    for row in myreader:
      count += 1

      Invoice = {}
      Invoice['PK'] = row[0]
      Invoice['SK'] ='root'
      Invoice['InvoiceDate'] = row[1]
      Invoice['InvoiceBalance'] = row[2]
      Invoice['InvoiceStatus'] = row[3]
      Invoice['InvoiceDueDate']= row[4]
      Invoice_item = dynamodb_table.put_item(Item=Invoice)

      Invoice_Customer = {}
      Invoice_Customer['PK'] = row[0]
      Invoice_Customer['SK'] = row[9]
      Invoice_Customer_item = dynamodb_table.put_item(Item=Invoice_Customer)

      Bill_Invoice = {}
      Bill_Invoice['PK'] = row[0]
      Bill_Invoice['SK'] = row[5]
      Bill_Invoice['BillAmount'] = row[7]
      Bill_Invoice['BillBalance'] = row[8]
      Bill_Invoice_item = dynamodb_table.put_item(Item=Bill_Invoice)

      Customer={}
      Customer['PK'] = row[9]
      Customer['SK'] = row[0]
      Customer['CustomerName'] = row[10]
      Customer['State'] = row[11]
      Customer_item = dynamodb_table.put_item(Item=Customer)

      Bill = {}
      Bill['PK'] = row[5]
      Bill['SK'] = row[0]
      Bill['BillDueDate'] = row[6]
      Bill['BillAmount'] = row[7]
      Bill_item = dynamodb_table.put_item(Item=Bill)

      if count % 100 == 0:
        time2 = time.time() - time1
        print("Entry count: %s in %s" % (count, time2))
        time1 = time.time()
    return count

if __name__ == "__main__":
    args = sys.argv[1:]
    tableName = args[0]
    fileName = args[1]

    #### Capture the execution begin time ####
    begin_time = time.time()

    #### Call the function to Import data into the DynamoDb Table ####
    count = import_csv(tableName, fileName)

    #### Print Execution Summary ####
    print('RowCount: %s, Total seconds: %s' %(count, (time.time() - begin_time)))
