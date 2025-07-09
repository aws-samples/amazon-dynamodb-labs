---
title : "Full Migration"
weight : 32
---

## DynamoDB Import from S3

The Import from S3 feature is a convenient way to have data loaded into a new DynamoDB table. 
Learn more about this feature [here](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/S3DataImport.HowItWorks.html).

Import creates a brand new table, and is not able to load data into an existing table.
Therefore, it is most useful during the one-time initial load of data during a migration.

## migrate.sh

A script is provided that performs multiple steps to coordinate a migration:
* Runs **mysql_desc_ddb.py** and stores the result in a table definition JSON file
* Runs **mysql_s3.py** to extract, transform, and load data into an S3 bucket
* Uses the **aws dynamodb import-table** CLI command to request a new table, by providing the bucket name and table definition JSON file

1. Run:
```bash
./migrate.sh Customers
```
The script should produce output as shown here:

![Migrate Output](/static/images/relational-migration/migrate_output.png)

Notice the ARN returned. This is the ARN of the Import job, not the new DynamoDB table.

The import will take a few minutes to complete. 

2. Optional: You can check the status of an import job using this command, by setting the Import ARN on line two.

```bash
aws dynamodb describe-import \
    --import-arn '<paste ARN here>' \
    --output json --query '{"Status         ":ImportTableDescription.ImportStatus, "FailureCode    ":ImportTableDescription.FailureCode, "FailureMessage ":ImportTableDescription.FailureMessage }'
```

We can also check the import status within the AWS Console.

3. Click into the separate browser tab titled "AWS Cloud9" to open the AWS Console.
4. In the search box, type DynamoDB to visit the DyanmoDB console.
5. From the left nav, click Imports from S3.
6. Notice your import is listed along with the current status. 
7. Once the import has completed, you can click it to see a summary including item count and the size of the import.
8. On the left nav, click to Tables.
9. In the list of tables, click on the Customers table.
10. On the top right, click on Explore Table Items.
11. Scroll down until you see a grid with your imported data.

Congratulations! You have completed a relational-to-DynamoDB migration.
