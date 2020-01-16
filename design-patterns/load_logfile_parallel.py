from __future__ import print_function # Python 2/3 compatibility
import boto3
import time
import csv
import sys
import string
import random
import threading
import glob
from multiprocessing import Queue
from lab_config import boto_args

queue = Queue()

def import_csv(tableName, filename, thread_id):
    dynamodb = boto3.resource(**boto_args)
    dynamodb_table = dynamodb.Table(tableName)
    count = 0

    batch_size = 250
    rows_of_file = 2000
    rows_of_thread = batch_size * rows_of_file
    SHARDS = 10

    time1 = time.time()
    with open(filename, 'r', encoding="utf-8") as csvfile:
        myreader = csv.reader(csvfile, delimiter=',')
        for row in myreader:
            with dynamodb_table.batch_writer() as batch:
                for i in range(batch_size):
                    count += 1

                    newitem = {}
                    newitem['requestid'] = (thread_id * rows_of_thread) + (i * rows_of_file) + int(row[0])
                    newitem['host'] = row[1]
                    newitem['date'] =  row[2]
                    newitem['hourofday'] = int(row[3])
                    newitem['timezone'] = row[4]
                    newitem['method'] = row[5]
                    newitem['url'] = row[6]
                    newitem['responsecode'] = int(row[7])
                    newitem['bytessent'] = int(row[8])
                    newitem['useragent'] = row[9]

                    # Set primary keys
                    if tableName == "logfile_gsi_low":
                        newitem["GSI_1_PK"] = "host#{}".format(newitem['host'])
                    else:
                        newitem['GSI_1_PK'] = "shard#{}".format((newitem['requestid'] % SHARDS) + 1)
                        newitem['GSI_1_SK'] = row[7] + "#" + row[2] + "#" + row[3]

                    newitem['PK'] = "request#{}".format((thread_id * rows_of_thread) + (i * rows_of_file) + int(row[0]))

                    batch.put_item(Item=newitem)
                    if count % 5000 == 0:
                        time2 = time.time() - time1
                        print("thread_id: %s, row: %s, %s" % (thread_id, count, time2))
                        time1 = time.time()
    queue.put(count)

if __name__ == "__main__":
    args = sys.argv[1:]
    tableName = args[0]

    thread_list = []

    begin_time = time.time()
    # BUGFIX https://github.com/boto/boto3/issues/1592
    boto3.resource(**boto_args)
    #
    files = glob.glob("./data/logfile_medium*.csv")
    thread_id = 0
    for f in files:
        print("starting thread for file: %s" % (f))
        thread = threading.Thread(target=import_csv, args=(tableName, f, thread_id))
        thread_list.append(thread)
        thread_id += 1
        time.sleep(.2)

    # Start threads
    for thread in thread_list:
        thread.start()

    # Block main thread until all threads are finished
    for thread in thread_list:
        thread.join()

    totalcount = 0
    for t in range(len(files)):
        totalcount = totalcount + queue.get()

    print('total rows %s in %s seconds' %(totalcount, time.time() - begin_time))
