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
    | Table mappings: Editing mode | Select JSON editor option and follow the instructions after below screenshots|

  ![Final Deployment Architecture](/images/migration25.jpg)
  ![Final Deployment Architecture](/images/migration26.jpg)

  In this section we will create Table mappings JSON document. This document includes source to target mapping including any transformation on the records that will be performed during migration.
  To reduce the loading time during Immersion Day, we have narrowed down the migration list to selective movies. Below JSON document has list of 28 movies worked by Clint Eastwood.
  The remaining exercise will just focus on these movies. However, feel free to load remaining data in case you like to further explore.
  Some statistics around full dataset is give at the bottom of this chapter.

Copy list of selective movies by Clint Eastwood.
```json
    {
      "filter-operator": "eq",
      "value": "tt0309377"
    },
    {
      "filter-operator": "eq",
      "value": "tt12260846"
    },
    {
      "filter-operator": "eq",
      "value": "tt1212419"
    },
    {
      "filter-operator": "eq",
      "value": "tt1205489"
    },
    {
      "filter-operator": "eq",
      "value": "tt1057500"
    },
    {
      "filter-operator": "eq",
      "value": "tt0949815"
    },
    {
      "filter-operator": "eq",
      "value": "tt0824747"
    },
    {
      "filter-operator": "eq",
      "value": "tt0772168"
    },
    {
      "filter-operator": "eq",
      "value": "tt0498380"
    },
    {
      "filter-operator": "eq",
      "value": "tt0418689"
    },
    {
      "filter-operator": "eq",
      "value": "tt0405159"
    },
    {
      "filter-operator": "eq",
      "value": "tt0327056"
    },
    {
      "filter-operator": "eq",
      "value": "tt2310814"
    },
    {
      "filter-operator": "eq",
      "value": "tt2179136"
    },
    {
      "filter-operator": "eq",
      "value": "tt2083383"
    },
    {
      "filter-operator": "eq",
      "value": "tt1924245"
    },
    {
      "filter-operator": "eq",
      "value": "tt1912421"
    },
    {
      "filter-operator": "eq",
      "value": "tt1742044"
    },
    {
      "filter-operator": "eq",
      "value": "tt1616195"
    },
    {
      "filter-operator": "eq",
      "value": "tt6997426"
    },
    {
      "filter-operator": "eq",
      "value": "tt6802308"
    },
    {
      "filter-operator": "eq",
      "value": "tt3513548"
    },
    {
      "filter-operator": "eq",
      "value": "tt3263904"
    },
    {
      "filter-operator": "eq",
      "value": "tt3031654"
    },
    {
      "filter-operator": "eq",
      "value": "tt8884452"
    }
  ```
  Below JSON document will migrate denormalized view from imdb MySQL database (Task identified: historical-migration01).
  Replace the string "REPLACE THIS STRING BY MOVIES LIST" with list of movies copied earlier (Checkout following screenshot for any confusion).
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
        "rule-action": "include",
        "filters": [
          {
            "filter-type": "source",
            "column-name": "tconst",
            "filter-conditions": ["REPLACE THIS STRING BY MOVIES LIST"]
          }
        ]
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
  ![Final Deployment Architecture](/images/migration36.png)
  Go to the bottom and click on Create task. At this point the task will create will automatically start loading selective movies from source to target DynamoDB table.
  You can move forward and create two more tasks with similar steps (historical-migration02 and historical-migration03).
  Keep rest of the parameter as is except the JSON document. For historical-migration02 and historical-migration03 tasks use the JSON document mentioned below.

  Below JSON document will migrate title_akas table from imdb MySQL database (Task identified: historical-migration02)
  Replace the string "REPLACE THIS STRING BY MOVIES LIST" with list of movies copied earlier.
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
              "rule-action": "include",
              "filters": [
                {
                  "filter-type": "source",
                  "column-name": "titleId",
                  "filter-conditions": ["REPLACE THIS STRING BY MOVIES LIST"]
                }
              ]
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
Below JSON document will migrate title_ratings table from imdb MySQL database (Task identified: historical-migration03)
Replace the string "REPLACE THIS STRING BY MOVIES LIST" with list of movies copied earlier.
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
            "rule-action": "include",
            "filters": [
              {
                "filter-type": "source",
                "column-name": "tconst",
                "filter-conditions": ["REPLACE THIS STRING BY MOVIES LIST"]
              }
            ]
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
The replication job for historical migration will start moving data from MySQL imdb.movies view, title_akas and title_ratings to DynamoDB table will start in a few minutes.
If you are loading selective records based on the list above, it may take 5-10 minutes to complete all three jobs. For full loading below are the statistics.
  - historical-migration01 job will migrate 800K+ records and normally takes 2-3 Hrs.
  - historical-migration02 job will migrate 747K+ records and normally takes 2-3 Hrs.
  - historical-migration03 job will migrate 79K+ records and normally takes 10-15 Minutes.
You can track the status of data loading under the Table statistics of the migration task. Once loading is in progress, feel free to move to the next section of the exercise.
![Final Deployment Architecture](/images/migration27.jpg)
