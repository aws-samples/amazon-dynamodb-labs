---
title: "Explore Source Model"
menuTitle: "Explore Source Model"
date: 2021-04-25T07:33:04-05:00
weight: 30
---
IMDb [(Internet Movie Database)](https://www.imdb.com/interfaces/) is one of the most recognized names for its comprehensive online database collection of movies, films, TV series and so on.
The exercise is going to use subset of IMDb dataset (available in TSV format). This workshop will utilize 6 IMDb dataset that are related to US based movies since year 2000.
The dataset has around 106K+ movies, ratings, votes and cast/crew information.

The CloudFormation template has launched EC2 Amazon Linux 2 instance with MySQL installed and running.
It has created imdb database, 6 new tables (one for each IMDb dataset), downloaded IMDb TSV files to MySQL server local directory and uploaded the files to 6 new tables. To explore dataset, follow below instructions to login EC2 server.
It has also configured a remote MySQL user based on the CloudFormation input parameter.

 1. Go to [EC2 console](https://console.aws.amazon.com/ec2/v2/home?region=us-east-1#Instances:instanceState=running)
 2. Select the MySQL-Instance and click Connect
    ![Final Deployment Architecture](/images/migration9.jpg)
 3. Make sure ec2-user is filled under the User name field. Click Connect
    ![Final Deployment Architecture](/images/migration10.jpg)
 4. Elevate your privilege using sudo command
    ```bash
      sudo su
    ```
    ![Final Deployment Architecture](/images/migration11.jpg)
 5. Go to the file directory
    ```bash
      cd /var/lib/mysql-files/
      ls -lrt
    ```
 6. You can see all the 6 files copied from the IMDB dataset to the local EC2 directory
    ![Final Deployment Architecture](/images/migration12.jpg)
 7. Feel free to explore the files.
 8. Go to AWS CloudFormation [Stacks](https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks?filteringStatus=active&filteringText=&viewNested=true&hideStacks=false) and click on the stack you created earlier. Go to the Parameters tab and copy the user name and password mentioned next to DbMasterUsername & DbMasterPassword
   ![Final Deployment Architecture](/images/migration13.jpg)
 9. Go back to EC2 Instance console and login to mysql
  ```bash
  mysql -u DbMasterUsername -pDbMasterPassword
  ```
   ![Final Deployment Architecture](/images/migration14.jpg)
10. Congratulations! You are now connected to a self-managed MySQL source database on EC2. In next steps, we will explore database and tables hosting IMDb datasets
  ```bash
  use imdb;
  ```
   ![Final Deployment Architecture](/images/migration15.jpg)
11. Show all the tables created;
   ```bash
   show tables;
   ```
   ![Final Deployment Architecture](/images/migration16.jpg)

For illustration purpose, below is a logical diagram represents relationship between various source tables hosting IMDb dataset.

  - title_basics table has movies published in US after year 2000. tconst is an alphanumeric key uniquely assigned to each movie.
  - title_akas has published regions, languages and respective movie titles. It's 1:many relationship with title_basics table.
  - title_ratings has movies rating and vote count. For this exercise, we can assume the information has high frequency update post movie release. It's 1:1 related with title_basics table
  - title_principals has cast and crew information. It's 1:many relationship with title_basics table.
  - title_crew has writer and director information. The table is 1:1 related with title_basics table.
  - name_basics has cast and crew details. Every member has unique nconst value assigned.
  ![Final Deployment Architecture](/images/migration31.jpg)

12. We will create denormalized view with 1:1 static information and get it ready for migration to Amazon DynamoDB table. For now, go ahead and copy below code and paste into the MySQL command line.
The details around target data model will be discussed in the next chapter.
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
  Use below command to review count of records from the denormalized view. At this point, your source database is ready to migrate to Amazon DynamoDB.
  ```bash
  select count(*) from imdb.movies;
  ```
