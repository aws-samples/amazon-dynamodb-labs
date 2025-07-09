---
title: "Exercise Overview"
menuTitle: "Exercise Overview"
date: 2021-04-25T07:33:04-05:00
weight: 10
---
In this module, you will create an environment to host the MySQL database on Amazon EC2. This instance will be used to host source database and simulate on-premise side of migration architecture.
All the resources to configure source infrastructure are deployed via [Amazon CloudFormation](https://aws.amazon.com/cloudformation/) template.
There are two CloudFormation templates used in this exercise which deploy the following resources.

CloudFormation MySQL Template Resources (**Already deployed**):
  - **OnPrem VPC**: Source VPC will represent an on-premise source environment in the workshop region. This VPC will host source MySQL database on Amazon EC2
  - **Amazon EC2 MySQL Database**: Amazon EC2 Amazon Linux 2 AMI with MySQL installed and running
  - **Load IMDb dataset**: The template will create IMDb database on MySQL and load IMDb public dataset files into database. You can learn more about IMDb dataset inside [Explore Source Model](/hands-on-labs/rdbms-migration/migration-chapter03)



CloudFormation DMS Instance Resources (**Needs deploying**):
  - **DMS VPC**:  Migration VPC in the workshop region. This VPC will host DMS replication instance.
  - **Replication Instance**: DMS Replication instance that will facilitate database migration from source MySQL server on EC2 to Amazon DynamoDB

![Final Deployment Architecture](/static/images/migration-environment.png)
