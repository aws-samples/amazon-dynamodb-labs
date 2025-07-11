---
title: "Load DynamoDB Table"
menuTitle: "Load DynamoDB Table"
date: 2021-04-25T07:33:04-05:00
weight: 50
---

In this exercise, we will set up Database Migration Service (DMS) jobs to migrate data from source MySQL database (relational view, tables) to Amazon DynamoDB.

## Verify DMS creation

1. Go to [DMS Console](https://console.aws.amazon.com/dms/v2/home?region=us-east-1#dashboard) and click on **Replication Instances**. You should be able to see a replication instance with **Class** `dms.c5.2xlarge` in `Available` **Status**.
    ![Final Deployment Architecture](/static/images/migration20.jpg)

::alert[_Make sure the DMS instance is Available before you continue. If it is not Available, return to the CloudFormation console to review and troubleshoot the CloudFormation stack._]

## Update inbound rules for MySQL instance security group to allow access from DMS IP

1. Select the `mysqltodynamo-instance` DMS replication instance, copy its **Public IP address**.

![Copy DMS Public IP](/static/images/migration52.png)

2. Open [EC2 console](https://console.aws.amazon.com/ec2/v2/home#Instances:instanceState=running), select **MySQL-Instance**. Under the **Security** tab, select the security group of the MySQL instance (eg: `sg-xxxxx`).

![Open MySQL EC2 Security Group](/static/images/migration53.png)

3. Select **Edit inbound rules**, then **Add rule**. Select **MYSQL/Aurora** in **Type**, and paste the Public IP address of the MySQL Instance with a `/32` suffix. For example, for IP `54.X.X.X`, enter `54.X.X.X/32` in **Source**. Finally, select **Save rules**.

![Edit inbound rules of Security Group](/static/images/migration54.png)

## Create source and target endpoints

1.  From the DMS console, select **Endpoints** and then **Create endpoint**.
    ![Final Deployment Architecture](/static/images/migration21.jpg)
2.  Create the source endpoint. Use the following parameters to configure the endpoint:

    | Parameter           |                                                                                 Value                                                                                 |
    | ------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------: |
    | Endpoint type       |                                                                            Source endpoint                                                                            |
    | Endpoint identifier |                                                                            mysql-endpoint                                                                             |
    | Source engine       |                                                                                 MySQL                                                                                 |
    | Access to endpoint database |                                         Select the "Provide access information manually" radio button                                                         |
    | Server name         | From the [EC2 dashboard](https://console.aws.amazon.com/ec2/v2/home#Instances:instanceState=running), select MySQL-Instance and copy Public IPv4 DNS |
    | Port                |                                                                                 3306                                                                                  |
    | SSL mode            |                                                                                 none                                                                                  |
    | User name           |                                            Value of DbMasterUsername added as parameter during Configure MySQL Environment                                            |
    | Password            |                                            Value of DbMasterPassword added as parameter during Configure MySQL Environment                                            |

![Final Deployment Architecture](/static/images/migration22.jpg)

3. Open **Test endpoint connection (optional)** section, then in the **VPC** drop-down select **DMS-VPC** and click the **Run test** to verify that your endpoint configuration is valid. The test will run for a minute and you should see a *successful* message in the **Status** column. Click on the **Create endpoint** to create the endpoint. If you see a connection error, re-type the username and password to ensure no mistakes were made. Further, ensure you provided the IPv4 DNS name ending in `amazonaws.com` in the field **Server name**.

![Final Deployment Architecture](/static/images/migration23.jpg)

4. Create the target endpoint. Repeat all steps to create the target endpoint with the following parameter values:

    | Parameter               |                                                                                            Value                                                                                            |
    | ----------------------- | :-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: |
    | Endpoint type           |                                                                                       Target endpoint                                                                                       |
    | Endpoint identifier     |                                                                                      dynamodb-endpoint                                                                                      |
    | Target engine           |                                                                                       Amazon DynamoDB                                                                                       |
    | Service access role ARN | CloudFormation template has created new role with full access to Amazon DynamoDB. Copy Role ARN from [dynamodb-access](https://us-east-1.console.aws.amazon.com/iamv2/home#/roles/details/dynamodb-access?section=permissions) role |

![Final Deployment Architecture](/static/images/migration24.jpg)

5. Open **Test endpoint connection (optional)** section, then in the **VPC** drop-down select **DMS-VPC** and select **Run test** to verify that your endpoint configuration is valid. The test will run for a minute and you should see a *successful* message in the **Status** column. Click **Create endpoint** to create the endpoint.

## Configure and Run a Replication Task

Still in the AWS DMS console, go to **Database migration tasks** and click on **Create database migration task**. We will create 3 replication jobs to migrate denormalized view, ratings (`title_ratings`) and regions/languages (`title_akas`) information.

1. Task1: Enter the following parameter values in the Create database migration task screen:

   | Parameter                                    |                                     Value                                     |
   | -------------------------------------------- | :---------------------------------------------------------------------------: |
   | Task identifier                              |                            historical-migration01                             |
   | Replication instance                         |                          mysqltodynamodb-instance-\*                          |
   | Source database endpoint                     |                                mysql-endpoint                                 |
   | Target database endpoint                     |                               dynamodb-endpoint                               |
   | Migration type                               |                             Migrate existing data                             |
   | Task settings: Editing mode                  |                                    Wizard                                     |
   | Task settings: Target table preparation mode |                                  Do nothing                                   |
   | Task settings: Turn on CloudWatch logs       |                                    Checked                                    |
   | Table mappings: Editing mode                 | Select JSON editor option and follow the instructions after below screenshots |

![Final Deployment Architecture](/static/images/migration25.jpg)
![Final Deployment Architecture](/static/images/migration26.jpg)

Start with the JSON editor section open in your browser. In this section we will create Table mappings JSON document to replace what you see in the JSON editor. This document includes source to target mapping including any transformation on the records that will be performed during migration.
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

Below JSON document will migrate denormalized view from imdb MySQL database (Task identifier: `historical-migration01`).
Replace the string “REPLACE THIS STRING BY MOVIES LIST” with list of movies copied earlier (Checkout following screenshot for any confusion). Then paste the resulting JSON code in to the JSON editor, replacing the existing code.
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

![Final Deployment Architecture](/static/images/migration36.png)

::alert[Make sure the **Turn on premigration assessment** is un-checked. For MySQL based source databases, AWS DMS supports running a bunch of validations as part of a premigration assessment like if binlog compression is disabled, or DMS has replication priveleges. Full list in [AWS Documentation](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Tasks.AssessmentReport.MySQL.html).]

Go to the bottom and click on **Create database migraton task**. At this point the task will be created and will automatically start loading selected movies from source to target DynamoDB table. 
You can move forward and create two more tasks with similar steps (`historical-migration02` and `historical-migration03`).
Use the same settings as above except the Table Mappings JSON document. For `historical-migration02` and `historical-migration03` tasks use the JSON document mentioned below.

Below JSON document will migrate title_akas table from imdb MySQL database (Task identifier: `historical-migration02`)
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

Below JSON document will migrate title_ratings table from imdb MySQL database (Task identifier: `historical-migration03`)
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
#### Solutions 
::::expand{header="If you are having trouble with making the JSON documents for the tasks, expand this section to get the solutions!"}

-   [First Task - historical-migration01](:assetUrl{path="/files/hands-on-labs/Task_1.json"})
-   [Second Task - historical-migration02](:assetUrl{path="/files/hands-on-labs/Task_2.json"})
-   [Third Task - historical-migration03](:assetUrl{path="/files/hands-on-labs/Task_3.json"})
::::

### Monitor and the restart/resume the tasks
The replication task for historical migration will start moving data from MySQL `imdb.movies` view, `title_akas` and `title_ratings` to DynamoDB table will start in a few minutes.
If you are loading selective records based on the list above, it may take 5-10 minutes to complete all three tasks.

If you were to run this exercise again but do a full load, the load times would be as follows:
- historical-migration01 task will migrate 800K+ records and normally takes 2-3 Hrs.
- historical-migration02 task will migrate 747K+ records and normally takes 2-3 Hrs.
- historical-migration03 task will migrate 79K+ records and normally takes 10-15 Minutes.  


You can track the status of data loading under the Table statistics of the migration task. Once loading is in progress, feel free to move to the next section of the exercise.
  ![Final Deployment Architecture](/static/images/migration27.jpg)

::alert[_Make sure all tasks are running or complete before you continue. If a task says **Ready**, check its box and choose "Restart/Resume" under the Actions button to start the task._]

