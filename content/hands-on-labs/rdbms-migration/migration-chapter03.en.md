+++
title = "Explore Source Data"
menuTitle = "Explore Source Data"
date = 2021-04-25T07:33:04-05:00
weight = 30
+++
IMDb [(Internet Movie Database)](https://www.imdb.com/interfaces/) is one of the most recognized names for its comprehensive online database collection of movies, films, TV series and so on.
The exercise is going to use subset of IMDb dataset. This workshop will utilize 6 IMDb dataset that are related to US based movies since year 2000. Each dataset is already loaded into 6 tables on MySQL imdb database deployed using previous CloudFormation template.
The dataset has around 106K+ movies and crew information.

Using CloudFormation template, you have launched EC2 Amazon Linux 2 instance with MySQL installed and running. The template has also created new imdb database, 6 tables (one for each IMDb dataset), loaded dataset into the tables and a new remote MySQL user based on the CloudFormation input parameter.
The copy of the IMBb dataset (TSV files) is also copied into the local file directory at EC2 server. To explore dataset follow below instructions to login to EC2 server.

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
 6. You can see all the 6 files copied from the IMDB dataset to the local EC2 directory
    ![Final Deployment Architecture](/images/migration12.jpg)
 8. Feel free to explore the files.
 9. Go to AWS CloudFormation [Stacks](https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks?filteringStatus=active&filteringText=&viewNested=true&hideStacks=false) and click on the stack you created earlier. Go to the Parameters tab and copy the user name and password mentioned next to DbMasterUsername & DbMasterPassword
   ![Final Deployment Architecture](/images/migration13.jpg)
10. Go back to EC2 Instance console and login to mysql
  ```bash
  mysql -u DbMasterUsername -pDbMasterPassword
  ```
   ![Final Deployment Architecture](/images/migration14.jpg)
11. Congratulations! you are now connected to a self-managed MySQL source database on EC2. In next steps we will explore database and tables hosting IMDb datasets
  ```bash
  use imdbUSE imdb;
  ```
   ![Final Deployment Architecture](/images/migration15.jpg)
12. Show all the tables created;
   ```bash
   show tables;
   ```
   ![Final Deployment Architecture](/images/migration16.jpg)

For illustration purpose, below logical diagram represents relationaship between various source tables hosting IMDb dataset.
  1.  title_basics table has all movies published in US after year 2000. tconst is an alphanumeric key uniquely assigned to each movies.
  2.  title_akas holds information related to various region and language that movie was originally published. This has 1:many relationshify with title_basics table.
  3.  title_ratings holds information related to average movies rating and vote count. We can assume this has dynamic information that can change over time post movies are published.
  4.  title_principals has information related to various crew member worked inside the movie. The table has 1:many relationship with title_basics table.
  5.  title_crew has information related to writer and director for movies. The table is 1:1 related with title_basics table.
  6.  name_basics has information related to all crew members and thier primary professions. Every actor has unique nconst value assigned.
![Final Deployment Architecture](/images/migration31.jpg)
