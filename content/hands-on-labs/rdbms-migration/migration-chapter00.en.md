+++
title = "Excercise Overview"
menuTitle = "Excercise Overview"
date = 2021-04-25T07:33:04-05:00
weight = 10

+++
In this module, you will create an environment to host the MySQL database on Amazon EC2. This instance will be used as a source database and help to simulate on-premise relational database structure.
The resources are deployed via [Amazon CloudFormation](https://aws.amazon.com/cloudformation/) template. The CloudFromation will deploy the following resources as shown in the diagram.
  - OnPrem VPC: Source VPC will represent an on-premise source environment in the N. Virginia region. This VPC will host source MySQL database on Amazon EC2
  - DMS VPC: DMS VPC will host DMS replication instances in the N. Virginia region. This replication instance will facilitate database migration from source MySQL server to Amazon DynamoDB
  - Amazon EC2 MySQL Database: Amazon EC2 Amazon Linux 2 AMI with MySQL installed and running
![Final Deployment Architecture](/images/migration-environment.png)
