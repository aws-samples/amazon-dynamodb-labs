+++
title = "Load DynamoDB Table"
menuTitle = "Load DynamoDB Table"
date = 2021-04-25T07:33:04-05:00
weight = 50

+++
In this excercise we will setup Database Migration Service(DMS) jobs to migrate data from source denormalized relational view to Amazon DynamoDB.

 1. Go to IAM console > Roles > Create Role
 2. Under AWS Services, Select DMS > Next Permissions
 3. Attach AmazonDMSVPCManagementRole policy
 4. Next Tag, skip this step
 5. Next Review, add role name as dms-vpc-role and click Create role
 6. Download the [CloudFormation](/files/hands-on-labs/migration-dms-setup.yaml) template
 7. Open [CloudFormation](https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/create/template), click on Create Stack and select With new resources (standard)
 8. Select Template source as Upload a template file and choose the downloaded yaml file
   ![Final Deployment Architecture](/images/migration17.jpg)
 4. Click Next
 5. Provide Stack Name and Update Parameters
   ![Final Deployment Architecture](/images/migration18.jpg)
 6. Click Next
 7. Check I acknowledge and click Create stack. The CloudFormation template will take 5-10 minutes to build replication envirorment. You can monitor the progress using stack status.
   ![Final Deployment Architecture](/images/migration19.jpg)
 9. Once CloudFormation stack status shows CREATE_COMPLETE, go to [DMS Console](https://console.aws.amazon.com/dms/v2/home?region=us-east-1#dashboard)  and click on Replication Instances. You can able to see replication instance with Class dms.c5.2xlarge in Available Status.
   ![Final Deployment Architecture](/images/migration20.jpg)
## Create source and target endpoints

 1.  Go back to AWS Console, AWS Database Migration Service screen, click on Endpoints and Create endpoint button
   ![Final Deployment Architecture](/images/migration21.jpg)
 2.  Create the source endpoint. Use the following parameters to configure the endpoint:
     | Parameter        | Value |
     | ------------- |:-------------:|
     | Endpoint type     | Source endpoint|
     | Endpoint identifier     | mysql-endpoint|
     | Source engine     | MySQL|
     | Server name     | From the [EC2 dashboard](https://console.aws.amazon.com/ec2/v2/home?region=us-east-1#Instances:instanceState=running), select MySQL-Instance and copy Public IPv4 DNS|
     | Port     | 3306|
     | SSL mode     | none|
     | User name     | Value of DbMasterUsername added as parameter during Configure MySQL Environment|
     | Password    | Value of DbMasterPassword added as parameter during Configure MySQL Environment|

     ![Final Deployment Architecture](/images/migration22.jpg)
     Open Test endpoint connection (optional) section, then in the VPC drop-down select DMS-VPC and click the Run test button to verify that your endpoint configuration is valid.Test will run for a minute and you should see successful message in the Status column. Click on the Create endpoint button to create the endpoint.
     ![Final Deployment Architecture](/images/migration23.jpg)
  3. Create the target endpoint. Repeat all steps to create the target endpoint with the following parameter values:
     | Parameter        | Value |
     | ------------- |:-------------:|
     | Endpoint type     | Target endpoint|
     | Endpoint identifier     | dynamodb-endpoint|
     | Target engine     | Amazon DynamoDB|
     | Service access role ARN     | CloudFormation template has created new role with full access to Amazon DynamoDB. Copy Role ARN from [dynamodb-access](https://console.aws.amazon.com/iam/home#/roles/dynamodb-access) role|

     ![Final Deployment Architecture](/images/migration24.jpg)
     Open Test endpoint connection (optional) section, then in the VPC drop-down select DMS-VPC and click the Run test button to verify that your endpoint configuration is valid.Test will run for a minute and you should see successful message in the Status column. Click on the Create endpoint button to create the endpoint.

   ## Configure and Run a Replication Task

  Still in the AWS DMS console, go to Database migration tasks and click the Create Task button.
  1. Enter the following parameter values in the Create database migration task screen:
    | Parameter        | Value |
    | ------------- |:-------------:|
    | Task identified     | historical-migration|
    | Replication instance     | mysqltodynamodb-instance-*|
    | Source database endpoint     | mysql-endpoint|
    | Target database endpoint     | dynamodb-endpoint|
    | Migration type     | Migrate existing data|
    | Enable CloudWatch logs | Checked |
    | Table mappings | Select JSON editor option and copy the JSON document mentioned below|
    | Start task on create     | Checked|

  ```json

      {
          "rules": [
              {
                  "rule-type": "selection",
                  "rule-id": "1",
                  "rule-name": "1",
                  "object-locator": {
                      "schema-name": "imdb",
                      "table-name": "dynamo_migration",
                      "table-type": "view"
                  },
                  "rule-action": "include"
              },
              {
                  "rule-type": "object-mapping",
                  "rule-id": "2",
                  "rule-name": "2",
                  "rule-action": "map-record-to-record",
                  "object-locator": {
                      "schema-name": "imdb",
                      "table-name": "dynamo_migration",
                      "table-type": "view"
                  },
                  "target-table-name": "dynamo_migration",
                  "mapping-parameters": {
                      "partition-key-name": "tconst",
                      "sort-key-name": "tconst_orderning",
                      "exclude-columns": [],
                      "attribute-mappings": [
                          {
                              "target-attribute-name": "tconst",
                              "attribute-type": "scalar",
                              "attribute-sub-type": "string",
                              "value": "${tconst}"
                          },
                          {
                              "target-attribute-name": "tconst_orderning",
                              "attribute-type": "scalar",
                              "attribute-sub-type": "string",
                              "value": "${category}|${nconst}|${ordering}"
                          }
                      ]
                  }
              }
          ]
      }
  ```

![Final Deployment Architecture](/images/migration25.jpg)
![Final Deployment Architecture](/images/migration26.jpg)
The replication job for historical migration will start moving data from MySQL dynamo_migration denormalized view to DynamoDB table in few minutes. The job will migration 2.5 millions records and normally takes 4-5 Hrs..
You can track status of data loading under Table statistics of migration task. Once loading is in progress, feel free to move to the next section of the excercise.
![Final Deployment Architecture](/images/migration27.jpg)
