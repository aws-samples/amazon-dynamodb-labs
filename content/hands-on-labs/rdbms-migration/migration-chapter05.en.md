+++
title = "Load DynamoDB Table"
menuTitle = "Load DynamoDB Table"
date = 2021-04-25T07:33:04-05:00
weight = 50

+++
In this exercise, we will set up Database Migration Service (DMS) jobs to migrate data from source MySQL database (relational view, tables) to Amazon DynamoDB.

 1. Go to IAM console > Roles > Create Role
 2. Under AWS Services, Select DMS > Next Permissions
 3. Attach AmazonDMSVPCManagementRole policy
 4. Next Tag, skip this step
 5. Next Review, add role name as dms-vpc-role and click Create role
 6. Download the [CloudFormation](/files/hands-on-labs/migration-dms-setup.yaml) template
 7. Open [CloudFormation](https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/create/template), click on Create Stack and select with new resources (standard)
 8. Select Template source as Upload a template file and choose the downloaded yaml file
   ![Final Deployment Architecture](/images/migration17.jpg)
 9. Click Next
 10. Provide Stack Name and Update Parameters
   ![Final Deployment Architecture](/images/migration18.jpg)
 11. Click Next
 12. Check I acknowledge and click Create stack. The CloudFormation template will take 5-10 minutes to build a replication environment. You can monitor the progress using stack status.
   ![Final Deployment Architecture](/images/migration19.jpg)
 13. Once CloudFormation stack status shows CREATE_COMPLETE, go to [DMS Console](https://console.aws.amazon.com/dms/v2/home?region=us-east-1#dashboard)  and click on Replication Instances. You can able to see a replication instance with Class dms.c5.2xlarge in Available Status.
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
     Open Test endpoint connection (optional) section, then in the VPC drop-down select DMS-VPC and click the Run test button to verify that your endpoint configuration is valid. The test will run for a minute and you should see a successful message in the Status column. Click on the Create endpoint button to create the endpoint.
     ![Final Deployment Architecture](/images/migration23.jpg)
  3. Create the target endpoint. Repeat all steps to create the target endpoint with the following parameter values:
     | Parameter        | Value |
     | ------------- |:-------------:|
     | Endpoint type     | Target endpoint|
     | Endpoint identifier     | dynamodb-endpoint|
     | Target engine     | Amazon DynamoDB|
     | Service access role ARN     | CloudFormation template has created new role with full access to Amazon DynamoDB. Copy Role ARN from [dynamodb-access](https://console.aws.amazon.com/iam/home#/roles/dynamodb-access) role|

     ![Final Deployment Architecture](/images/migration24.jpg)
     Open Test endpoint connection (optional) section, then in the VPC drop-down select DMS-VPC and click the Run test button to verify that your endpoint configuration is valid. The test will run for a minute and you should see a successful message in the Status column. Click on the Create endpoint button to create the endpoint.

   ## Configure and Run a Replication Task

  Still in the AWS DMS console, go to Database migration tasks and click the Create Task button. We will create 3 replication jobs to migrate denormalized view, ratings (title_ratings) and regions/languages (title_akas) information.
  1. Task1: Enter the following parameter values in the Create database migration task screen:
    | Parameter        | Value |
    | ------------- |:-------------:|
    | Task identified     | historical-migration01|
    | Replication instance     | mysqltodynamodb-instance-*|
    | Source database endpoint     | mysql-endpoint|
    | Target database endpoint     | dynamodb-endpoint|
    | Migration type     | Migrate existing data|
    | Task settings: Editing mode  | Wizard|
    | Task settings: Target table preparation mode | Do nothing|
    | Task settings: Enable CloudWatch logs | Checked |
    | Table mappings: Editing mode | Select JSON editor option and paste JSON document as mentioned below|

JSON document to migrate denormalized view from imdb MySQL database (Task identified: historical-migration01)
  ```json

      {
          "rules": [
              {
                  "rule-type": "selection",
                  "rule-id": "1",
                  "rule-name": "1",
                  "object-locator": {
                      "schema-name": "imdb",
                      "table-name": "movies",
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
                      "table-name": "movies",
                      "table-type": "view"
                  },
                  "target-table-name": "movies",
                  "mapping-parameters": {
                      "partition-key-name": "mpkey",
                      "sort-key-name": "mskey",
                      "exclude-columns": [],
                      "attribute-mappings": [
                          {
                              "target-attribute-name": "mpkey",
                              "attribute-type": "scalar",
                              "attribute-sub-type": "string",
                              "value": "${tconst}"
                          },
                          {
                              "target-attribute-name": "mskey",
                              "attribute-type": "scalar",
                              "attribute-sub-type": "string",
                              "value": "DETL|${category}|${ordering}"
                          }
                      ]
                  }
              }
          ]
      }
  ```
  JSON document to migrate title_akas table from imdb MySQL database (Task identified: historical-migration02)

  ```json
    {
      "rules": [
          {
              "rule-type": "selection",
              "rule-id": "1",
              "rule-name": "1",
              "object-locator": {
                  "schema-name": "imdb",
                  "table-name": "title_akas",
                  "table-type": "table"
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
                  "table-name": "title_akas",
                  "table-type": "table"
              },
              "target-table-name": "movies",
              "mapping-parameters": {
                  "partition-key-name": "mpkey",
                  "sort-key-name": "mskey",
                  "exclude-columns": [],
                  "attribute-mappings": [
                      {
                          "target-attribute-name": "mpkey",
                          "attribute-type": "scalar",
                          "attribute-sub-type": "string",
                          "value": "${titleId}"
                      },
                      {
                          "target-attribute-name": "mskey",
                          "attribute-type": "scalar",
                          "attribute-sub-type": "string",
                          "value": "REGN|${region}"
                      }
                  ]
              }
          }
      ]
    }
  ```
JSON document to migrate title_ratings table from imdb MySQL database (Task identified: historical-migration03)
  ```json

  {
    "rules": [
        {
            "rule-type": "selection",
            "rule-id": "1",
            "rule-name": "1",
            "object-locator": {
                "schema-name": "imdb",
                "table-name": "title_ratings",
                "table-type": "table"
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
                "table-name": "title_ratings",
                "table-type": "table"
            },
            "target-table-name": "movies",
            "mapping-parameters": {
                "partition-key-name": "mpkey",
                "sort-key-name": "mskey",
                "exclude-columns": [],
                "attribute-mappings": [
                    {
                        "target-attribute-name": "mpkey",
                        "attribute-type": "scalar",
                        "attribute-sub-type": "string",
                        "value": "${tconst}"
                    },
                    {
                        "target-attribute-name": "mskey",
                        "attribute-type": "scalar",
                        "attribute-sub-type": "string",
                        "value": "RTNG"
                    }
                ]
            }
        }
      ]
    }
  ```

![Final Deployment Architecture](/images/migration25.jpg)
![Final Deployment Architecture](/images/migration26.jpg)
You need to create two more tasks with similar steps (historical-migration02 and historical-migration03).
Don't change any other parameter except the Table mappings Editing mode.
For historical-migration02 and historical-migration03 tasks use the JSON document mentioned below.
The replication job for historical migration will start moving data from MySQL imdb.movies view, title_akas and title_ratings to DynamoDB table will start in a few minutes.
  - historical-migration01 job will migrate 800K+ records and normally takes 2-3 Hrs.
  - historical-migration02 job will migrate 747K+ records and normally takes 2-3 Hrs.
  - historical-migration03 job will migrate 79K+ records and normally takes 10-15 Minutes.
You can track the status of data loading under the Table statistics of the migration task. Once loading is in progress, feel free to move to the next section of the exercise.
![Final Deployment Architecture](/images/migration27.jpg)
