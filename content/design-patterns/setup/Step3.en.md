+++
title = "Step 3 - Check boto3 installation"
date = 2019-12-02T10:07:52-08:00
weight = 30
+++


Boto3 is the Amazon Web Services (AWS) Software Development Kit (SDK) for Python, which allows Python developers to build applications using AWS services.

In the EC2 shell window, run ```python``` to make an interactive console with the first command and then copy and paste the following Python code:
```bash
# Open python:
python
 ```
```py
# Run this code:
import boto3
ddb = boto3.client('dynamodb')
ddb.describe_limits()
```


You will see the following result:
```txt
{u'TableMaxWriteCapacityUnits': 40000, u'TableMaxReadCapacityUnits': 40000, u'AccountMaxReadCapacityUnits': 80000, 'ResponseMetadata': {'RetryAttempts': 0, 'HTTPStatusCode': 200, 'RequestId': 'BFMGAS4P48I3DJTP5NU22QRDDJVV4KQNSO5AEMVJF66Q9ASUAAJG', 'HTTPHeaders': {'x-amzn-requestid': 'BFMGAS4P48I3DJTP5NU22QRDDJVV4KQNSO5AEMVJF66Q9ASUAAJG', 'content-length': '143', 'server': 'Server', 'connection': 'keep-alive', 'x-amz-crc32': '3062975651', 'date': 'Tue, 31 Dec 2020 00:00:00 GMT', 'content-type': 'application/x-amz-json-1.0'}}, u'AccountMaxWriteCapacityUnits': 80000}
```
To close Python console, type:
```py
quit()
```
