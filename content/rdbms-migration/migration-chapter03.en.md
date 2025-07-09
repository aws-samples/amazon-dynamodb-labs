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
The CloudFormation template also configured a remote MySQL user based on input parameters for the template. 
To explore the dataset, follow the instructions below to log in to the EC2 server.

 1. Go to [EC2 console](https://console.aws.amazon.com/ec2/v2/home#Instances:instanceState=running).
 2. Select the MySQL Instance and click **Connect**.
    ![Final Deployment Architecture](/static/images/migration9.jpg)
 3. Make sure `ec2-user` is in the **User name** field. Click **Connect**.
    ![Final Deployment Architecture](/static/images/migration10.jpg)
 4. Elevate your privileges using the `sudo` command.
    ```bash
      sudo su
    ```
    ![Final Deployment Architecture](/static/images/migration11.jpg)
 5. Go to the file directory.
    ```bash
      cd /var/lib/mysql-files/
      ls -lrt
    ```
 6. You can see all the 6 files copied from the IMDB dataset to the local EC2 directory.
    ![Final Deployment Architecture](/static/images/migration12.jpg)
 7. Feel free to explore the files.
 8. Go to [AWS CloudFormation Console](https://console.aws.amazon.com/cloudformation/home#/stacks?filteringStatus=active&filteringText=&viewNested=true&hideStacks=false) and click on the stack you created earlier. Go to the **Parameters** tab and copy the username and password listed next to **DbMasterUsername** and **DbMasterPassword**.
   ![Final Deployment Architecture](/static/images/migration13.jpg)
 9. Go back to EC2 Instance console and login to mysql.
  ```bash
  mysql -u DbMasterUsername -pDbMasterPassword
  ```
   ![Final Deployment Architecture](/static/images/migration14.jpg)
10. Congratulations! You are now connected to a self-managed MySQL source database on EC2. In the following steps, we will explore the database and tables hosting IMDb datasets.
  ```bash
  use imdb;
  ```
   ![Final Deployment Architecture](/static/images/migration15.jpg)
11. List all the tables created by the CloudFormation stack.
   ```bash
   show tables;
   ```
   ![Final Deployment Architecture](/static/images/migration16.jpg)

For illustration purposes, below is a logical diagram represents relationship between various source tables hosting IMDb dataset.

  - `title_basics` has movies published in the US after the year 2000. `tconst` is an unique alphanumeric key assigned to each movie.
  - `title_akas` has published regions, languages, and the respective movie titles. It has a 1\:many relationship with the `title_basics` table.
  - `title_ratings` has movies rating and vote count. For this exercise, we can assume the information has high frequency updates post movie release. It has a 1:1 relationship with the `title_basics` table.
  - `title_principals` has cast and crew information. It has a 1\:many relationship with the `title_basics` table.
  - `title_crew` has writer and director information. It has a 1:1 relationship with the `title_basics` table.
  - `name_basics` has cast and crew details. Every member has unique `nconst` value assigned.
  ![Final Deployment Architecture](/static/images/migration31.jpg)

12. We will create a denormalized view with 1:1 static information and get it ready for migration to Amazon DynamoDB table. For now, go ahead and copy the code below and paste into the MySQL command line.
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
