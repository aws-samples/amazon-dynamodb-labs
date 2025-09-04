---
title: "6.4 Creating Glue Jobs"
menuTitle: "Creating Glue Jobs"
date: 2025-09-02T16:43:04-05:00
weight: 34
chapter: false
---

## Building the Data Movement Engine

Now comes the exciting part - creating the actual machines that will move your data from MySQL to DynamoDB. These "machines" are called AWS Glue jobs, and they're like smart robots that can read data from one place, transform it according to your rules, and write it to another place.

Think of this step as building and deploying the moving trucks that will transport your belongings from your old house (MySQL) to your new house (DynamoDB), making sure everything gets organized properly during the move.

## What Are AWS Glue Jobs?

AWS Glue jobs are automated scripts that run in the cloud to process your data. For this migration, each job will:

- **Read from MySQL Views**: Use the views you created to get properly formatted data
- **Apply Transformations**: Convert the data according to your migration contract
- **Write to DynamoDB**: Insert the transformed data into your new tables
- **Handle Errors**: Deal with any issues that come up during the transfer
- **Report Progress**: Let you know how the migration is going

Each job is written in Python using PySpark (a framework for processing large amounts of data quickly). Don't worry - the system generates all this code automatically based on your migration contract.

## The Job Creation Process

### Step 1: Generate Python Scripts

The automation process will create specialized Python scripts for each of your tables. These scripts contain all the logic needed to:

- Connect to your MySQL database using the views you created
- Read data in batches to handle large datasets efficiently  
- Transform the data format from MySQL to DynamoDB
- Write the data to the correct DynamoDB tables
- Handle any errors or data quality issues

![Migration control panel](/static/images/modernizr/6/stage06-14.png)

You'll see Cline creating files with names like:
- `users_migration.py` - Handles migrating user data
- `product_migration.py` - Handles migrating product data  
- `categories_migration.py` - Handles migrating category data

### Step 2: Upload Supporting Files

Once the Python scripts are created, they need to be stored in Amazon S3 (cloud storage) where Glue can access them. This is like putting your moving instructions in a place where all the moving trucks can read them.

![Migration control panel](/static/images/modernizr/6/stage06-15.png)

The system will upload each script file to S3, making sure they're in the right location with the correct permissions for Glue to use them. The process also uploads any supporting files the jobs might need, such as configuration files or utility libraries. This ensures the jobs have everything they need to run successfully.

![Migration control panel](/static/images/modernizr/6/stage06-16.png)

Please notice the workflow needs to run this process 3 times, once for each table. 

### Step 3: Create the Glue Jobs

Finally, the system creates the actual Glue jobs in AWS. Each job is configured with:

- **Script Location**: Where to find the Python code in S3
- **Database Connection**: How to connect to your MySQL database
- **DynamoDB Permissions**: Authorization to write to your tables
- **Resource Allocation**: How much computing power to use
- **Error Handling**: What to do if something goes wrong

![Migration control panel](/static/images/modernizr/6/stage06-17.png)

Remember to approve each job creation when Cline asks - this gives you control over the process and lets you review what's being created.

### Step 4: Verifying Job Creation

After all jobs are created, you can see them in the AWS Glue console. They should appear as "Ready" and waiting to be executed.

![Migration control panel](/static/images/modernizr/6/stage06-18.png)

You'll see three jobs corresponding to your three tables:
- **Users ETL Job**: Ready to migrate user data
- **Products ETL Job**: Ready to migrate product data
- **Categories ETL Job**: Ready to migrate category data

Each job is like a loaded moving truck, ready to start the migration when you give the signal.

### Step 5: Start the Data Migration

You have complete control over when to start the actual data migration. For this workshop, we'll start the migration immediately while your application is still using MySQL (Phase 1 of your feature flags from Stage 5).

This approach is safe because:
- Your application continues running normally on MySQL
- The migration happens in the background
- You can validate the DynamoDB data before switching over
- If anything goes wrong, your application is unaffected

![Migration control panel](/static/images/modernizr/6/stage06-19.png)

When you approve the job executions, all three jobs will start running simultaneously, each handling its portion of the data migration.

### Step 6: Monitor Progress

Once the jobs start, you can watch their progress in the AWS Glue console. You'll see real-time information about:

- **Job Status**: Running, completed, or failed
- **Records Processed**: How many items have been migrated
- **Processing Speed**: How fast the migration is progressing
- **Error Count**: Any issues that need attention

![Migration control panel](/static/images/modernizr/6/stage06-20.png)

The jobs will process your data in parallel, which means the migration completes faster than if you moved each table one at a time.

### Step 7: Completion Confirmation

When all jobs finish successfully, the system will notify you that the migration is complete.

![Migration control panel](/static/images/modernizr/6/stage06-21.png)

This completion message means:
- All your MySQL data has been successfully transformed
- The data has been written to the correct DynamoDB tables
- The format matches your migration contract specifications
- No critical errors occurred during the process

## Validating the Migration

### Step 8: Verify Your Data

The final step is to check that your data actually made it to DynamoDB. Go to the AWS DynamoDB console and look at your tables - they should now contain data.

![Migration control panel](/static/images/modernizr/6/stage06-22.png)

For each table, verify:
- **Item Count**: Should match (approximately) the number of records in your MySQL tables
- **Data Format**: Items should have the structure defined in your migration contract
- **Key Values**: Partition keys and sort keys should be populated correctly
- **Attributes**: All the expected data fields should be present

With your data successfully migrated to DynamoDB, you're ready to start testing your dual-database system and begin the controlled transition from MySQL to DynamoDB using the feature flag system you built in Stage 5.
