+++
title = "Step 7 - Low capacity GSI"
date = 2019-12-02T10:26:31-08:00
weight = 8
+++


For the next step, let's create a new table with different capacity units. For the purpose of this exercise, the GSI will have only 1 WCU and 1 RCU.

Run the following command:
```bash
aws dynamodb create-table --table-name logfile_gsi_low \
--attribute-definitions AttributeName=PK,AttributeType=S AttributeName=GSI_1_PK,AttributeType=S \
--key-schema AttributeName=PK,KeyType=HASH \
--provisioned-throughput ReadCapacityUnits=1000,WriteCapacityUnits=1000 \
--tags Key=workshop-design-patterns,Value=targeted-for-cleanup \
--global-secondary-indexes "IndexName=GSI_1,\
KeySchema=[{AttributeName=GSI_1_PK,KeyType=HASH}],\
Projection={ProjectionType=INCLUDE,NonKeyAttributes=['bytessent']},\
ProvisionedThroughput={ReadCapacityUnits=1,WriteCapacityUnits=1}"
```
Run the command to wait until the table becomes Active:
```bash
aws dynamodb wait table-exists --table-name logfile_gsi_low
```
This command will create a new table and one GSI with the following definition:


#### Table: logfile_gsi_low

- Key schema: HASH
- Table RCU = 1000
- Table WCU = 1000
- GSI(s):
  - GSI_1 (**1 RCU, 1 WCU**) - *Allows for querying by host IP address.*



| Attribute name (Type)        | Special attribute?           | Attribute use case          | Sample attribute value  |
| ------------- |:-------------:|:-------------:| -----:|
| PK (STRING)      | Hash key | Holds the request id for the access log  | *request#104009*  |
| GSI_1_PK (STRING)      | GSI 1 hash key | The host for the request, an IPv4 address  | *host#66.249.67.3*  |



Let's populate this table with a large dataset. We will use a multi-threaded version of the Python load script to simulate a higher Writes Per Second to the DynamoDB table.
```bash
python load_logfile_parallel.py logfile_gsi_low
```
After a few minutes, the above script execution will be throttled and show an error message like below:
```txt
ProvisionedThroughputExceededException: An error occurred (ProvisionedThroughputExceededException) when calling the BatchWriteItem operation (reached max retries: 9): The level of configured provisioned throughput for one or more global secondary indexes of the table was exceeded. Consider increasing your provisioning level for the under-provisioned global secondary indexes with the UpdateTable API
```
**You can pause the operation by typing Ctrl+Z**

**Note:** *This new table has more RCU=1000 and WCU=1000 but we received an error and the load time increased.*

**Topics for discussion:** *Can you explain the behavior of the test?*

Open the AWS console to view the metrics for the table **logfile_gsi_low**. If you don't see the table, remember to click the refresh button on the top right of the DynamoDB console.

**Figure - Write capacity metric for the table**
![Write capacity metric for the table](/images/image2.jpg)

Note above that the consumed writes were below the provisioned writes for the table during the test.

**Figure - Write capacity metric for the GSI**
![Write capacity metric for the GSI](/images/image3.jpg)

Note above that the consumed writes were higher than the provisioned writes for the GSI.

**Figure - Throttled write requests for the table**
![Throttled writes for the table](/images/image4.jpg)

Note that the table shows throttled requests (*ThrottledRequests*), even though it was provisioned with sufficient Write Capacity Units.

To identify the source of the throttles, we must review the *WriteThrottleEvents* metric.

**Figure - Throttled write events on the GSI**
![Throttled writes for the GSI](/images/image5.jpg)

Remember to consider all the access patterns on the table (and secondary indexes) to determine the WCUs and RCUs to be provisioned on the table. Note that the GSIs have to be provisioned separately. An under-provisioned GSI may start to apply back pressure on the tables. Remember to monitor the required metrics on both the tables and the GSIs and set the monitoring alarms based on your business requirements.
