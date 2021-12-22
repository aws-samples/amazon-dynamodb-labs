+++
title = "Load Source Data"
menuTitle = "Load Source Data"
date = 2021-04-25T07:33:04-05:00
weight = 30

+++
Using CloudFormation template, you have launched EC2 Amazon Linux 2 instance with MySQL installed and running. The template has also created a new user based on the CloudFormation input parameter.
The script has copied the public IMDB dataset into the file directory at deployed EC2 server.
Learn more about [IMDB dataset](https://www.imdb.com/interfaces/).

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
 5. Go to the file diretory
    ```bash
      cd /var/lib/mysql-files/
      ls -lrt
    ```
 6. You can see all the 7 files copied from the IMDB dataset to the local EC2 directory
    ![Final Deployment Architecture](/images/migration12.jpg)
 8. Feel free to explore the files.
 9. Go to AWS CloudFormation [Stacks](https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks?filteringStatus=active&filteringText=&viewNested=true&hideStacks=false) and click on the stack you created earlier. Go to the Parameters tab and copy the user name and password mentioned next to DbMasterUsername & DbMasterPassword
   ![Final Deployment Architecture](/images/migration13.jpg)
10. Go back to EC2 Instance console and login to mysql
  ```bash
  mysql -u DbMasterUsername -pDbMasterPassword
  ```
   ![Final Deployment Architecture](/images/migration14.jpg)
11. Congratulations! you are now connected to a self-managed MySQL database on EC2. We will create a new imdb database and load datasets that are available as flat file on EC2 directory
  ```bash
  CREATE DATABASE imdb;
  USE imdb;
  ```
   ![Final Deployment Architecture](/images/migration15.jpg)
12. Type below command to create source tables inside imdb Database
   ```bash
   CREATE TABLE title_akas (titleId VARCHAR(200), ordering VARCHAR(200),title VARCHAR(1000), region VARCHAR(1000), language VARCHAR(1000), types VARCHAR(1000),attributes VARCHAR(1000),isOriginalTitle VARCHAR(5),primary key (titleId, ordering));
   CREATE TABLE imdb.title_basics (tconst  VARCHAR(200), titleType  VARCHAR(1000),primaryTitle  VARCHAR(1000), originalTitle  VARCHAR(1000), isAdult  VARCHAR(1000), startYear  VARCHAR(1000),endYear  VARCHAR(1000),runtimeMinutes  VARCHAR(1000),genres  VARCHAR(1000),primary key (tconst));
   CREATE TABLE title_crew (tconst  VARCHAR(200), directors  VARCHAR(1000),writers  VARCHAR(1000),primary key (tconst));
   CREATE TABLE title_episode (tconst  VARCHAR(200), parentTconst  VARCHAR(1000),seasonNumber  integer, episodeNumber  integer,primary key (tconst));
   CREATE TABLE title_principals (tconst  VARCHAR(200), ordering  VARCHAR(200),nconst  VARCHAR(200), category  VARCHAR(1000), job  VARCHAR(1000), characters  VARCHAR(1000),primary key (tconst,ordering,nconst));
   CREATE TABLE title_ratings (tconst  VARCHAR(200), averageRating float,numVotes  integer,primary key (tconst));
   CREATE TABLE name_basics (nconst  VARCHAR(200), primaryName  VARCHAR(1000),birthYear  VARCHAR(1000), deathYear  VARCHAR(1000), primaryProfession  VARCHAR(1000), knownForTitles VARCHAR(1000),primary key (nconst));
   ```
13. Show all the tables created;
   ```bash
   show tables;
   ```
   ![Final Deployment Architecture](/images/migration16.jpg)
14. Type below command to load data from flatfiles to MySQL imdb database. The process will take 20-30 minutes to load entire dataset.
  ```bash
   LOAD DATA INFILE '/var/lib/mysql-files/title_ratings.tsv' IGNORE INTO TABLE imdb.title_ratings FIELDS TERMINATED BY '\t';
   LOAD DATA INFILE '/var/lib/mysql-files/title_basics.tsv'  IGNORE INTO TABLE imdb.title_basics FIELDS TERMINATED BY '\t';
   LOAD DATA INFILE '/var/lib/mysql-files/title_crew.tsv' IGNORE INTO TABLE imdb.title_crew FIELDS TERMINATED BY '\t';
   LOAD DATA INFILE '/var/lib/mysql-files/title_principals.tsv' IGNORE INTO TABLE imdb.title_principals FIELDS TERMINATED BY '\t';
   LOAD DATA INFILE '/var/lib/mysql-files/name_basics.tsv' IGNORE INTO TABLE imdb.name_basics FIELDS TERMINATED BY '\t';
   LOAD DATA INFILE '/var/lib/mysql-files/title_akas.tsv' IGNORE INTO  TABLE imdb.title_akas FIELDS TERMINATED BY '\t';
   ```
