---
title: "Access DynamoDB Table"
menuTitle: "Access DynamoDB Table"
date: 2021-04-25T07:33:04-05:00
weight: 60
---
Amazon DynamoDB supports [PartiQL](https://partiql.org/), a SQL-compatible query language, to select, insert, update, and delete data in Amazon DynamoDB.
Using PartiQL, you can easily interact with DynamoDB tables and run ad hoc queries using the AWS Management Console. In this exercise, we will hands-on a few access patterns using PartiQL statements.

  1. Login to [DynamoDB console](https://console.aws.amazon.com/dynamodbv2/home) and select PartiQL editor from left navigation.
  2. Select movies table that was created and loaded by the Database Migration Service job. Select ellipsis next to the table name and click on the scan table.
  ![Final Deployment Architecture](/images/migration28.jpg)
We will use PartiQL scripts to demonstrate all 6 access patterns discussed at previous chapter. For our example we will provide you the partition key values, but in real life you will need to make an index of keys perhaps using a GSI.
Get details by the movie: Each IMDB movie has a unique tconst. The denormalized table is created with each row representing a unique combination of movie and crew i.e. tconst and nconst.
Since tconst is part of the partition key for the base table, it can use under WHERE conditions to select the details. Copy below command to run inside PartiQL query editor.
  ![Final Deployment Architecture](/images/migration35.png)
  - Find all the cast and crew worked in a movie. Below query will include actor, actress, producer, cinematographer etc. worked in a given movie.
  ```bash
    SELECT * FROM "movies"
    WHERE "mpkey" = 'tt0309377' and begins_with("mskey",'DETL|')
  ```
  - Find only actors worked in a movie.

  ```bash
    SELECT * FROM "movies"
    WHERE "mpkey" = 'tt0309377' and begins_with("mskey",'DETL|actor')
  ```
  - Find only details of a movie.

  ```bash
    SELECT * FROM "movies"
    WHERE "mpkey" = 'tt0309377' and begins_with("mskey",'DETL|') and "ordering" = '1'
  ```
  - Find all the regions, languages and title for a movie.

  ```bash
    SELECT * FROM "movies"
    WHERE "mpkey" = 'tt0309377' and begins_with("mskey",'REGN|')
  ```
  - Find movie title for a specific region of a movie.

  ```bash
    SELECT * FROM "movies"
    WHERE "mpkey" = 'tt0309377' and begins_with("mskey",'REGN|NZ')
  ```
  - Find original title of a movie.

  ```bash
    SELECT * FROM "movies"
    WHERE "mpkey" = 'tt0309377' and begins_with("mskey",'REGN|') and "types" = 'original'
  ```
To access information at the crew member level (#6 in the access pattern), we need to create an additional Global Secondary Index (GSI) with a new partition key nconst (unique for crew member).
This will allow querying on the new partition key for GSI vs scan on the base table.

  3.  Select the Tables from the left navigation, choose movies table and click on the Index tab.
  4.  Click on Create Index and add the following details.


| Parameter        | Value |
| ------ |:-------------:|
| Partition key     | nconst|
| Data type     | String|
| Sort key - optional     | startYear|
| Data type     | String|
| Attribute projections     | All |

![Final Deployment Architecture](/images/migration29.jpg)
![Final Deployment Architecture](/images/migration30.jpg)

  5.  Finally, click on Create Index. This may take an hour depending on the number of records in the base table.
  6.  Once the GSI status columns change from Pending to Available, go back to the PartiQL editor to execute a query on GSI.

  - Find all movies by a crew (as actor, director etc.)

```bash
  SELECT * FROM "movies"."nconst-startYear-index"
  WHERE "nconst" = 'nm0000142'
```
- Find all movies by a crew as actor since 2002 and order by year ascending

```bash
  SELECT * FROM "movies"."nconst-startYear-index"
  WHERE "nconst" = 'nm0000142' and "startYear" >= '2002'
  ORDER BY "startYear"
```
Congratulations! you have completed the RDBMS migration exercise. 
