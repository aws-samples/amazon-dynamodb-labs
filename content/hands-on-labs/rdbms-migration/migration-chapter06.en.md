+++
title = "Access DynamoDB Table"
menuTitle = "Access DynamoDB Table"
date = 2021-04-25T07:33:04-05:00
weight = 60

+++

Amazon DynamoDB supports [PartiQL](https://partiql.org/), a SQL-compatible query language, to select, insert, update, and delete data in Amazon DynamoDB.
Using PartiQL, you can easily interact with DynamoDB tables and run ad hoc queries using the AWS Management Console. In this excercise we will hands-on few access pattern using PartiQL statements.

Go to [DynamoDB console](https://console.aws.amazon.com/dynamodbv2/home) and select PartiQL editor from left navigation.
You can able to see dynamo_migration table that was created and loaded by Database Migration Service job. Select ellipsis next to the table name and click on scan table.
You can scroll down to see records loaded via DMS job. Feel free to spend some time to explore dataset.
![Final Deployment Architecture](/images/migration28.jpg)
Using this excercise, we will review 4 unique access pattern on the base table and Global Secondary Index (GSI)
  - By Movie Queries (Base table)
    - Get details by movie
    - Get actors by movie

  - By Actors Queries (Global Secondary Index)
    - Get details by crew members
    - Get list of movies by an actor

Get details by movie: Each IMDB movie has unique tconst. The denormalized table is created with each row representing unique combination of movie and crew i.e. tconst and nconst.
Since tconst is part of partition key for the base table, it can use under WHERE condition to select the details. Copy below command to run inside PartiQL query editor.

  ```bash
  SELECT originalTitle, runtimeMinutes, averageRating, genres
  FROM "dynamo_migration"
  WHERE "tconst" = 'tt0310025' and ordering = '1'
  ```
Get crew member details by movie: Since data is flattened based on unique combination of movie and crew i.e. tconst and nconst, query by partition key (tconst) can provide list of all crew members associated with the movie.
```bash
    SELECT primaryName, primaryProfession, birthYear, deathYear
    FROM "dynamo_migration"
    WHERE "tconst" = 'tt0310025'
```
To access information at crew member level, we need to create additional Global Secondary Index(GSI) with new partition key than base table.
This will allow to query on new partition key for GSI vs scan on base table. Each crew members are uniquely identified by nconst field.
Select the Tables from the left navigation, choose dynamo_migration table and click on Index tab.
Click on Creat Index and add following details.
| Parameter        | Value |
| ------------- |:-------------:|
| Partition key     | nconst|
| Data type     | string|
| Sort key - optional     | category|
| Data type     | string|
| Attribute projections     | All |

![Final Deployment Architecture](/images/migration29.jpg)
![Final Deployment Architecture](/images/migration30.jpg)
Finally, click on Create Index. This may take 5-10 minutes depending on number of records in the base table.
Once the GSI status columns Available, go back to the PartiQL editor to execute query on GSI.

Get details by crew members: You can query new GSI created based on partition key to identify list of movies by a crew member.
```bash
    TBD
```
Get list of movies by an actor
```bash
    TBD
```
Congratulations! you have completed RDBMS migration excercise.
