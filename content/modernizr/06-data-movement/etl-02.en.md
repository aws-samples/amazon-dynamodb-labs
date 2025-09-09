---
title: "6.2 Creating MySQL views"
menuTitle: "Creating MySQL views"
date: 2025-09-02T16:43:04-05:00
weight: 32
chapter: false
---

## Preparing Your Data for Migration

Now that the connectivity is working, you need to prepare your MySQL data for the migration process. Think of this step like organizing your belongings before moving to a new house - you want to see how everything will look in the new format before actually moving it.

You'll create MySQL views that show your relational data in a denormalized format - exactly how it will appear in DynamoDB. This preview helps you catch any issues with your migration contract before running the actual data transfer.

## What Are MySQL Views?

MySQL views are like virtual tables that show data from your real tables in a different format. For this migration, the views will:

- **Combine Related Data**: Join information from multiple tables into single records
- **Apply Transformations**: Convert MySQL data types to DynamoDB-compatible formats
- **Test Your Migration Contract**: Verify that your transformation rules actually work with real data
- **Preview the Results**: Let you see exactly how your data will look in DynamoDB

The views act like a "dress rehearsal" for your migration - you can see the final result without actually changing anything in your production database.

### Step 1: Running the View Generation Process

Run the following command to start the automated view creation process:

```shell
Please execute all the tasks listed in this file `prompts/07-data-migration-execution/tasks.md`
```

![Migration control panel](/static/images/modernizr/6/stage06-07.png)

This command triggers Cline (the AI assistant) to read your migration contract from Stage 2 and automatically generate the MySQL views based on your data model specifications.

### Step 2: Watch the Automation Process

The system will start by creating an artifacts folder, then reading the `migrationContract.json` file from Stage 2. This process involves multiple rapid file operations that might seem fast, but remember that Cline has rate limits (4 executions per minute), so you may need to be patient or retry if something times out.

![Migration control panel](/static/images/modernizr/6/stage06-08.png)

Each step of the process is automated, but Cline will ask for your approval before executing each task. This safety mechanism ensures you can review what's happening before it makes changes to your database.

### Step 3: Approve Each View Creation

As the process runs, Cline will ask for permission to create each MySQL view. You'll see detailed explanations of what each view will do and how it transforms your data.

![Migration control panel](/static/images/modernizr/6/stage06-09.png)

The system creates one view at a time, allowing you to:
- **Review the SQL**: See exactly how each view combines and transforms your data
- **Understand the Logic**: Learn how relational data becomes NoSQL items
- **Catch Issues Early**: Spot problems with the transformation logic before migration

### Step 4: Test the Generated Views

After each view is created, you should manually query it to verify the results. This step is crucial - you need to confirm that:

- **Data Exists**: The views actually return records (not empty results)
- **Format is Correct**: The data matches your expected DynamoDB item structure  
- **Transformations Work**: MySQL data types are properly converted
- **Relationships are Preserved**: Related data is correctly combined

![Migration control panel](/static/images/modernizr/6/stage06-10.png)

Run queries like:
```sql
SELECT * FROM user_view LIMIT 10;
SELECT * FROM product_view LIMIT 10;
SELECT * FROM order_view LIMIT 10;
```

Each query should return data that looks like it's ready to be inserted into DynamoDB, with all the transformations from your migration contract applied.

With successful view creation and validation, you've proven that your migration contract works with real data. The next step will be to configure the AWS Glue ETL jobs that will use these views to actually migrate your data to DynamoDB.
