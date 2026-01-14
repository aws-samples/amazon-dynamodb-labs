---
title: "6.1 Testing Connectivity"
menuTitle: "Testing Connectivity"
date: 2025-09-02T16:43:04-05:00
weight: 31
chapter: false
---

## Setting Up the Data Pipeline

This workshop combines stages 6 and 7 to give you hands-on experience with both infrastructure deployment and the actual data movement process. Think of this as setting up both the roads and the trucks that will move your data from MySQL to DynamoDB.

The environment has been pre-configured with all the security permissions and network connectivity you need for the ETL (Extract, Transform, Load) process. However, you still need to provide the database password so the system can actually connect to your MySQL database.

From your workshop studio main page, locate on the bottom left the section "AWS account access" and click on "Open AWS console" as indicated in the picture below. This will open in a new tab the AWS console. 

:image[Migration control panel]{src="/static/images/modernizer/6/LGAM-06-stage06-1-01.png" disableZoom=true width=850}

In the search bar, located at the top left side of the screen, type "Glue. click on the AWS Glue Icon from the results. 

:image[Migration control panel]{src="/static/images/modernizer/6/LGAM-06-stage06-1-02.png" disableZoom=true width=850}

## Understanding AWS Glue

AWS Glue is Amazon's managed ETL service - it's like having a smart data processing robot that can:
- **Extract** data from your MySQL database
- **Transform** it using your migration contract rules
- **Load** it into DynamoDB in the correct format

The Glue scripts will use a pre-configured connection called `mysql-modernizer-connection` to securely connect to your database. This connection acts like a bridge between Glue and your MySQL server.

## Configuring the Database Connection

### Step 1: Access AWS Glue Console

In the left sidebar, click on **Data Connections** to see all available database connections.

:image[Migration control panel]{src="/static/images/modernizer/6/LGAM-06-stage06-1-03.png" disableZoom=true width=850}

### Step 2: Edit the MySQL Connection

Find the connection named `mysql-modernizer-connection` (1), select it. Click on the "Actions" drop down menu (2) and click **Edit** (3).

:image[Migration control panel]{src="/static/images/modernizer/6/LGAM-06-stage06-1-04.png" disableZoom=true width=850}

This connection has most of the settings already configured - you just need to add the password.

:image[Migration control panel]{src="/static/images/modernizer/6/LGAM-06-stage06-1-05.png" disableZoom=true width=850}

### Step 3: Add the Database Password

Retrieve the database password from the file `tools/config.json` (it should be around line 16). Enter this password in the connection configuration and click **Save**.

This password allows Glue to authenticate with your MySQL database. Without it, the ETL process can't access your data.

### Step 4: Verify Connectivity

Once the connection status shows "Ready", select the connection and click **Actions**, then **Test Connection**. 

:image[Migration control panel]{src="/static/images/modernizer/6/LGAM-06-stage06-1-06.png" disableZoom=true width=850}

To test the connection select the only IAM role that is available fromt the drop down list. 

:image[Migration control panel]{src="/static/images/modernizer/6/LGAM-06-stage06-1-07.png" disableZoom=true width=850}

This starts a connectivity validation process that typically takes about 1 minute.

:image[Migration control panel]{src="/static/images/modernizer/6/LGAM-06-stage06-1-08.png" disableZoom=true width=850}

The test creates a temporary network connection to your database to verify that:
- The network path is open
- Authentication works with the provided credentials
- Glue can successfully query the database schema

### Step 5: Confirm Success

You should receive a success message confirming the connection works properly. This green light means Glue can now access your MySQL database for the ETL process.

:image[Migration control panel]{src="/static/images/modernizer/6/LGAM-06-stage06-1-09.png" disableZoom=true width=850}

This successful connection test means your data pipeline is ready to begin extracting data from MySQL and transforming it according to your migration contract. You're ready to move on to the next step: generating the database views that will feed your ETL process.
