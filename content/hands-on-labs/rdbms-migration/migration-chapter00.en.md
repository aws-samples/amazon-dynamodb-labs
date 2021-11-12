+++
title = "Excercise Overview"
menuTitle = "Excercise Overview"
date = 2021-04-25T07:33:04-05:00
weight = 10

+++
In this module, you will create an environment to host MySQL database on Amazon EC2. This instance will be used as source database and help to simulate onpremise relational database structure.
The resources will be deployed via [Amazon CloudFormation](https://aws.amazon.com/cloudformation/) template. The CloudFromation will deploy following resorces as shown in the diagram.
  - OnPrem VPC: Source VPC will represent onpremise source environment in N. Virginia region. This VPC will host source MySQL database on Amazon EC2
  - DMS VPC: DMS VPC will host DMS replication instance in N. Virginia region. This replication instance will facilitate database migration from source MySQL server to Amazon DynamoDB
  - Amazon EC2 MySQL Database: Amazon EC2 Amazon Linux 2 AMI with MySQL installed and running
![Final Deployment Architecture](/images/migration-environment.png)
