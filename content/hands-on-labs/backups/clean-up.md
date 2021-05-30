+++
title = "Cleaning Up The Resources"
menuTitle = "Cleaning Up The Resources"
date = 2020-04-21T07:38:58-05:00
weight = 66
+++

If you used an account provided by Event Engine, you do not need to do any cleanup. The account terminates when the event is over.

If you used your own account,follow this [guide](https://docs.aws.amazon.com/aws-backup/latest/devguide/gs-cleanup-resources.html) to remove the following resources:


<li> Backup policy </li>
<li> Backup plans </li>
<li> Recovery points  </li>

Also, delete the three DynamoDB restored tables using following command.

```bash

aws dynamodb delete-table \
--table-name ProductCatalogODRestore

aws dynamodb delete-table \
--table-name ProductCatalogRestotred

aws dynamodb delete-table \
--table-name ProductCatalogPITR


```
