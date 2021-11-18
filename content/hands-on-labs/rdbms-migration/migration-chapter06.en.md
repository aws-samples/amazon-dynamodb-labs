+++
title = "Access DynamoDB Table"
menuTitle = "Access DynamoDB Table"
date = 2021-04-25T07:33:04-05:00
weight = 60

+++
Amazon DynamoDB supports [PartiQL](https://partiql.org/), a SQL-compatible query language, to select, insert, update, and delete data in Amazon DynamoDB.
Using PartiQL, you can easily interact with DynamoDB tables and run ad hoc queries using the AWS Management Console. In this exercise, we will hands-on a few access patterns using PartiQL statements.

Go to [DynamoDB console](https://console.aws.amazon.com/dynamodbv2/home) and select PartiQL editor from left navigation.
You can able to see dynamo_migration table that was created and loaded by the Database Migration Service job. Select ellipsis next to the table name and click on the scan table.
You can scroll down to see records loaded via the DMS job. Feel free to spend some time exploring the dataset.
![Final Deployment Architecture](/images/migration28.jpg)
Using this exercise, we will review 4 unique access patterns on the base table and Global Secondary Index (GSI)
  - By Movie Queries (Base table)
    - Get details by movie
    - Get actors by movie

  - By Actors Queries (Global Secondary Index)
    - Get details by crew members
    - Get a list of movies by an actor

Get details by the movie: Each IMDB movie has a unique tconst. The denormalized table is created with each row representing a unique combination of movie and crew i.e. tconst and nconst.
Since tconst is part of the partition key for the base table, it can use under WHERE conditions to select the details. Copy below command to run inside PartiQL query editor.

  ```bash
  SELECT originalTitle, runtimeMinutes, averageRating, genres
  FROM "dynamo_migration"
  WHERE "tconst" = 'tt0310025' and ordering = '1'
  ```
Get crew member details by the movie: Since data is flattened based on a unique combination of movie and crew i.e. tconst and nconst, query by partition key (tconst) can provide a list of all crew members associated with the movie.
```bash
    SELECT primaryName, primaryProfession, birthYear, deathYear
    FROM "dynamo_migration"
    WHERE "tconst" = 'tt0310025'
```
To access information at the crew member level, we need to create an additional Global Secondary Index(GSI) with a new partition key than the base table.
This will allow querying on the new partition key for GSI vs scan on the base table. Each crew member is uniquely identified by nconst field.
Select the Tables from the left navigation, choose dynamo_migration table and click on the Index tab.
Click on Create Index and add the following details.
| Parameter        | Value |
| ------------- |:-------------:|
| Partition key     | nconst|
| Data type     | string|
| Sort key - optional     | category|
| Data type     | string|
| Attribute projections     | All |

![Final Deployment Architecture](/images/migration29.jpg)
![Final Deployment Architecture](/images/migration30.jpg)
Finally, click on Create Index. This may take 5-10 minutes depending on the number of records in the base table.
Once the GSI status columns change from Pending to Available, go back to the PartiQL editor to execute a query on GSI.

Get details by crew members: You can query new GSI created based on a partition key to identify a list of movies by a crew member.
```bash
    SELECT primaryName,primaryProfession
    FROM "dynamo_migration"."nconst-category-index"
    WHERE "nconst" = 'nm2477166'
```
Get list of movies by an actor
```bash
    SELECT originalTitle
    FROM "dynamo_migration"."nconst-category-index"
    WHERE "nconst" = 'nm2477166' and "category" IN ['actor','actress']
```
Congratulations! you have completed the RDBMS migration exercise.
