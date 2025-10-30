---
title: "Explore Source Model"
menuTitle: "Explore Source Model"
date: 2021-04-25T07:33:04-05:00
weight: 30
---
IMDb [(Internet Movie Database)](https://www.imdb.com/interfaces/) is Amazon's comprehensive online database of movies, films, and TV series.
The workshop uses 6 IMDb datasets related to movies made in the United States since the year 2000.
The dataset has over 106K movies, ratings, votes, and cast/crew information.

The CloudFormation template launched an EC2 Amazon Linux 2 instance with MySQL installed and running.
It created a MySQL database called `imdb`, added 6 new tables (one for each IMDb dataset), downloaded the IMDb TSV files to MySQL server local directory, and loaded the file contents into the 6 tables. 

On the event dashboard, click on **Open AWS console** to federate into AWS Management Console in a new tab. On the same page, click **Get started** to open the workshop instructions.

![Event dashboard](/static/images/common/workshop-studio-01.png)

In addition to the AWS console you should open your Visual Studio code server, by clicking in the `VSCodeServerURL` parameter, available from the "Event Outputs" section. When prompted for a password use the value from `VSCodeServerPassword`. 

![Event dashboard](/static/images/common/workshop-studio-02.png)

During the first 60 seconds, the environment will automatically update extensions and plugins. Any startup notification can be safely dismissed. 
 
![VS Code Setup](/static/images/common/common-vs-code-01.png)

If a terminal is not available at the bottom left side of your screen, please open a new one like the following picture indicates.

![VS Code Setup](/static/images/common/common-vs-code-02.png)

In the terminal type:

```bash
cd LDMS

```

 If you are completing this workshop at an AWS hosted event, go to [AWS CloudFormation Console](https://console.aws.amazon.com/cloudformation/home#/stacks?filteringStatus=active&filteringText=&viewNested=true&hideStacks=false) and select the stack named **ddb**. Go to the **Parameters** tab and copy the username and password listed next to **DbMasterUsername** and **DbMasterPassword**.

 ::alert[_If you are completing this workshop in your AWS account copy the DbMasterUsername and DbMasterPassword from the CloudFormation stack used to configure the MySQL environment._]

   ![Final Deployment Architecture](/static/images/migration13.jpg)
 
 Go to the terminal and login to mysql.
  ```bash
   mysql -u dbuser -p 
  ```
 
   ![Final Deployment Architecture](/static/images/LMR/mysql-connecting.png)

Congratulations! You are now connected to a self-managed MySQL source database on EC2. In the following steps, we will explore the database and tables hosting IMDb datasets.
  
  ```bash
  use imdb;
  ```

   ![Final Deployment Architecture](/static/images/LMR/mysql-use-imdb.png)

List all the tables created by the CloudFormation stack.
   ```bash
   show tables;
   ```

   ![Final Deployment Architecture](/static/images/LMR/mysql-show-tables.png)

For illustration purposes, below is a logical diagram represents relationship between various source tables hosting IMDb dataset.

  - `title_basics` has movies published in the US after the year 2000. `tconst` is an unique alphanumeric key assigned to each movie.
  - `title_akas` has published regions, languages, and the respective movie titles. It has a 1\:many relationship with the `title_basics` table.
  - `title_ratings` has movies rating and vote count. For this exercise, we can assume the information has high frequency updates post movie release. It has a 1:1 relationship with the `title_basics` table.
  - `title_principals` has cast and crew information. It has a 1\:many relationship with the `title_basics` table.
  - `title_crew` has writer and director information. It has a 1:1 relationship with the `title_basics` table.
  - `name_basics` has cast and crew details. Every member has unique `nconst` value assigned.


![Final Deployment Architecture](/static/images/migration31.jpg)

We will create a denormalized view with 1:1 static information and get it ready for migration to Amazon DynamoDB table. For now, go ahead and copy the code below and paste into the MySQL command line.

We will discuss the details around the target data model in the next chapter.

```bash
CREATE VIEW imdb.movies AS\
    SELECT tp.tconst,\
           tp.ordering,\
           tp.nconst,\
           tp.category,\
           tp.job,\
           tp.characters,\
           tb.titleType,\
           tb.primaryTitle,\
           tb.originalTitle,\
           tb.isAdult,\
           tb.startYear,\
           tb.endYear,\
           tb.runtimeMinutes,\
           tb.genres,\
           nm.primaryName,\
           nm.birthYear,\
           nm.deathYear,\
           nm.primaryProfession,\
           tc.directors,\
           tc.writers\
    FROM imdb.title_principals tp\
    LEFT JOIN imdb.title_basics tb ON tp.tconst = tb.tconst\
    LEFT JOIN imdb.name_basics nm ON tp.nconst = nm.nconst\
    LEFT JOIN imdb.title_crew tc ON tc.tconst = tp.tconst;
  ```
  Use this command to check the count of records from the denormalized view. At this point, your source database is ready to migrate to Amazon DynamoDB.
  ```bash
  select count(*) from imdb.movies;
  ```
