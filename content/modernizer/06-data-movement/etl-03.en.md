---
title: "6.3 Creating DynamoDB Tables"
menuTitle: "Creating DynamoDB Tables"
date: 2025-09-02T16:43:04-05:00
weight: 33
chapter: false
---

::alert[Given the undeterministic nature of LLMs the steps below could be executed in a different order. Some of our workshop participants have got the creation of the views first followed by the creation of the DynamoDB tables, some others have got the creation of the DynamoDB tables first. Just follow your own environment and use the instructions here as a reference.]{type="info"}

## Building Your NoSQL Database Structure

Now that you have MySQL views showing how your data will look in DynamoDB format, it's time to create the actual DynamoDB tables that will store your migrated data. Think of this as building the containers that will hold your transformed data.

The system will use the DynamoDB MCP server to automatically create tables based on your migration contract specifications. This ensures the tables have exactly the right structure to receive the data from your ETL process.

## Understanding DynamoDB Table Creation

The automation process will create three main tables based on your migration contract:

- **Users Table**: With partition key (PK), sort key (SK), and the GSIs (Global Secondary Indexes) you designed in Stage 2
- **Products Table**: With its specific key structure and GSIs for product searches  
- **Categories Table**: With its keys and any necessary indexes for category operations

## Running the Table Creation Process

### Step 1: Automatic Execution

This table creation process should happen automatically as part of the initial migration command you ran. The system reads your migration contract and creates each table according to your specifications.

If the process stops or gets interrupted, you can simply ask Cline to `"continue with the creation of DynamoDB tables as indicated in task 1.1"`

### Step 2: Approve Each Table

For each table creation, Cline will ask for your approval and show you exactly what's being created. Pay attention to:

- **Table Names**: Ensure they match your expected naming (Users, Products, Categories)
- **Key Schema**: Verify the partition key (PK) and sort key (SK) are correct
- **GSI Configuration**: Check that all your planned indexes are included
- **Capacity Settings**: Confirm the read/write capacity makes sense for your data size

:image[Migration control panel]{src="/static/images/modernizer/6/LGAM-06-stage06-3-01.png" disableZoom=false width=425}

This approval step is important because once a DynamoDB table is created with a specific key schema, you can't change it without deleting and recreating the table.

### Step 3: Verifying Your Tables

Once all tables show as created, verify them in the AWS DynamoDB console. You should see your three tables: `Users`, `Products`, and `Categories`.

:image[Migration control panel]{src="/static/images/modernizer/6/LGAM-06-stage06-3-02.png" disableZoom=false width=850}

For each table, check:
- **Status**: Should be "ACTIVE" 
- **Key Schema**: Matches your migration contract specifications
- **GSIs**: All indexes are listed and active
- **Item Count**: Should be 0 (empty tables ready for data)

The tables are intentionally empty at this stage - they're like empty warehouses ready to receive inventory. The actual data will come from the ETL process in the next steps.

With your DynamoDB tables successfully created and active, you're ready to move to the next phase: configuring and running the ETL jobs that will actually move your data from MySQL to DynamoDB.
