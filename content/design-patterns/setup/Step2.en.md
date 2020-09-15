+++
title = "Step 2 - Check the Python and AWS CLI installation"
date = 2019-12-02T10:07:48-08:00
weight = 20
+++

Run the following command to check Python on your EC2 instance:

```bash
#Check the python version:
python --version
```
Output:
```plain
Python 3.6.12
```



Run the following command to check the AWS CLI on your EC2 instance:

```bash
#Check the AWS CLI version.
aws --version
```
Sample output:
```bash
#Note that your linux kernel version may differ from the example.
aws-cli/1.18.139 Python/3.6.12 Linux/4.14.193-113.317.amzn1.x86_64 botocore/1.17.62
```

**Note**: *Make sure you have AWS CLI version 1.18.139 and python 3.6.12 before proceeding. If you do not have these versions, review [Step 1]({{< ref "design-patterns/setup/Step1" >}}) to ensure you have completed each command correctly.*
