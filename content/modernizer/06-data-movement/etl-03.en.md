---
title: "6.3 Creating DynamoDB Tables"
menuTitle: "Creating DynamoDB Tables"
date: 2025-09-02T16:43:04-05:00
weight: 33
chapter: false
---

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

If the process stops or gets interrupted, you can simply ask Cline to "continue where you left off" or "restart the table creation process."

### Step 2: Approve Each Table

For each table creation, Cline will ask for your approval and show you exactly what's being created. Pay attention to:

- **Table Names**: Ensure they match your expected naming (Users, Products, Categories)
- **Key Schema**: Verify the partition key (PK) and sort key (SK) are correct
- **GSI Configuration**: Check that all your planned indexes are included
- **Capacity Settings**: Confirm the read/write capacity makes sense for your data size

![Migration control panel](/static/images/modernizer/6/stage06-11.png)

This approval step is important because once a DynamoDB table is created with a specific key schema, you can't change it without deleting and recreating the table.

### Step 3: Monitor Creation Status

After you approve each table, the MCP server will send the creation request to AWS. You'll see a response showing the table in "CREATING" status.

![Migration control panel](/static/images/modernizer/6/stage06-12.png)

The "CREATING" status means AWS is:
- **Allocating Resources**: Setting up the infrastructure to support your table
- **Configuring Keys**: Implementing your partition key and sort key structure
- **Building Indexes**: Creating your GSIs in the background
- **Setting Permissions**: Configuring access controls for your application

This process usually takes 1-3 minutes per table, depending on the complexity of your GSI configuration.

### Step 4: Verifying Your Tables

Once all tables show as created, verify them in the AWS DynamoDB console. You should see your three tables: `Users`, `Products`, and `Categories`.

![Migration control panel](/static/images/modernizer/6/stage06-13.png)

For each table, check:
- **Status**: Should be "ACTIVE" 
- **Key Schema**: Matches your migration contract specifications
- **GSIs**: All indexes are listed and active
- **Item Count**: Should be 0 (empty tables ready for data)

The tables are intentionally empty at this stage - they're like empty warehouses ready to receive inventory. The actual data will come from the ETL process in the next steps.

With your DynamoDB tables successfully created and active, you're ready to move to the next phase: configuring and running the ETL jobs that will actually move your data from MySQL to DynamoDB.
