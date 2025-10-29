---
title: "Step 2 - Check the Python and AWS CLI installation"
date: 2019-12-02T10:07:48-08:00
weight: 20
---

Run the following command to check Python on your EC2 instance:

```bash
#Check the python version:
python --version
```

Output:

```plain
Python 3.13.9
```
**Note: The major and minor version of Python may vary from what you see above**

Run the following command to check the AWS CLI on your EC2 instance:

```bash
#Check the AWS CLI version.
aws --version
```

Sample output:

```bash
#Note that your linux kernel version may differ from the example.
aws-cli/2.31.24 Python/3.13.7 Linux/6.1.155-176.282.amzn2023.aarch64 exe/aarch64.amzn.2023
```

::alert[_Make sure you have AWS CLI version 2.x or higher and python 3.10 or higher before proceeding. If you do not have these versions, you may have difficultly successfully completing the lab._]
