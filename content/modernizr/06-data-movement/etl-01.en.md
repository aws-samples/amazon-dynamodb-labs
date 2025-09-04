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

## Understanding AWS Glue

AWS Glue is Amazon's managed ETL service - it's like having a smart data processing robot that can:
- **Extract** data from your MySQL database
- **Transform** it using your migration contract rules
- **Load** it into DynamoDB in the correct format

The Glue scripts will use a pre-configured connection called `mysql-modernizr-connection` to securely connect to your database. This connection acts like a bridge between Glue and your MySQL server.

## Configuring the Database Connection

### Step 1: Access AWS Glue Console

Navigate to the AWS console and open the Glue service. In the left sidebar, click on **Data Connections** to see all available database connections.

![Migration control panel](/static/images/modernizr/6/stage06-02.png)

### Step 2: Edit the MySQL Connection

Find the connection named `mysql-modernizr-connection`, select it, and click **Edit**. This connection has most of the settings already configured - you just need to add the password.

![Migration control panel](/static/images/modernizr/6/stage06-03.png)

### Step 3: Add the Database Password

Retrieve the database password from the file `tools/config.json` (it should be around line 16). Enter this password in the connection configuration and click **Save**.

![Migration control panel](/static/images/modernizr/6/stage06-04.png)

This password allows Glue to authenticate with your MySQL database. Without it, the ETL process can't access your data.

## Testing the Connection

### Step 4: Verify Connectivity

Once the connection status shows "Ready", select the connection and click **Actions**, then **Test Connection**. This starts a connectivity validation process that typically takes about 1 minute.

![Migration control panel](/static/images/modernizr/6/stage06-05.png)

The test creates a temporary network connection to your database to verify that:
- The network path is open
- Authentication works with the provided credentials
- Glue can successfully query the database schema

### Step 5: Confirm Success

You should receive a success message confirming the connection works properly. This green light means Glue can now access your MySQL database for the ETL process.

![Migration control panel](/static/images/modernizr/6/stage06-06.png)

This successful connection test means your data pipeline is ready to begin extracting data from MySQL and transforming it according to your migration contract. You're ready to move on to the next step: generating the database views that will feed your ETL process.
