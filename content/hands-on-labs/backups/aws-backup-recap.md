+++
title = "AWS Backup Recap"
menuTitle = "AWS Backup Recap"
date = 2021-04-24T07:38:58-05:00
weight = 61
+++



AWS Backup is designed to help you to centralize and automate data
protection across AWS services. AWS Backup offers a cost-effective,
fully managed, policy-based service that further simplifies data
protection at scale. AWS Backup enables you to centrally deploy backup
policies to configure, manage, and govern your backup activity across
your organization’s AWS accounts and resources, including [Amazon
EC2](https://aws.amazon.com/ec2/) instances, [Amazon
EBS](https://aws.amazon.com/ebs) volumes, [Amazon
RDS](https://aws.amazon.com/rds/) databases , Amazon DynamoDB tables,
[Amazon EFS](https://aws.amazon.com/efs/), [Amazon FSx for
Lustre](https://aws.amazon.com/fsx/lustre/), [Amazon FSx for Windows
File Server](https://aws.amazon.com/fsx/windows/), and [AWS Storage
Gateway volumes](https://aws.amazon.com/storagegateway/volume/).

Let’s understand some AWS Backup terminology:

-   **Backup vault**: a container that you organize your backups in.

-   **Backup plan:** a policy expression that defines when and how you
    want to back up your AWS resources. The backup plan is attached to a
    **backup vault**.

-   **Resource assignment**: defines which resources should be backed
    up. You can select resources by tags or by resource ARN.

-   **Recovery point:** a snapshot/backup of a resource backed up by AWS
    Backup. Each recovery point can be restored with AWS Backup.
