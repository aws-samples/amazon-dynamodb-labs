+++
title = "Denormalized Schema Design"
menuTitle = "Denormalized Schema Design"
date = 2021-04-25T07:33:04-05:00
weight = 40

+++
Once flatfile are successfully loaded into imdb database, explore the source data based on data definition available over [IMDB website](https://www.imdb.com/interfaces/).

You can always perform lift and shift migration from relatational databases to DynamoDB using Database Migration Service.
Though, our focus in this excercise is to migrate subset of data in the most denormalized format possible. This will help to avoid any join during read operations and improve query performance.
Only subset of source data will be denormalized and moved to target DynamoDB tables. The degree of denormalization will highly depend upon the query access partterns.
In this excercise we will focus on designing denormalized MySQL view that will be migrated to DynamoDB. The concept is widely adopted in design principals followed during Customer 360.

Exploring the imdbdataset, you may notice tconst and nconst fields that is uniquely assigned to each movies and crew member respectively. We will use this primary key across all 7 tables to create joins
and pull subset of columns inside the target view. Also, to demonstrate row level filtering the view just filters all the movies published in english language.

Copy below code and paste into mysql command line
```bash
CREATE VIEW dynamo_migration AS\
	SELECT tp.tconst,\
		   tp.ordering,\
		   tb.primaryTitle,\
		   tb.originalTitle,\
		   tb.genres,\
		   tb.isAdult,\
		   tb.runtimeMinutes,\
		   tb.startYear,\
		   tb.titleType,\
		   te.episodeNumber,\
		   te.seasonNumber,\
		   te.parentTconst,\
		   tr.averageRating,\
		   tr.numVotes,\
		   tp.nconst,\
		   nm.primaryName,\
		   nm.birthYear,\
		   nm.deathYear,\
		   tp.category,\
		   tp.job,\
		   tp.characters,\
		   nm.primaryProfession\
	FROM imdb.title_principals tp\
	LEFT JOIN imdb.title_basics tb ON tp.tconst = tb.tconst\
	LEFT JOIN imdb.name_basics nm ON tp.nconst = nm.nconst\
	LEFT JOIN imdb.title_episode te ON te.tconst = tp.tconst\
	LEFT JOIN imdb.title_ratings tr ON tr.tconst = tp.tconst\
	LEFT JOIN imdb.title_akas ta ON ta.titleId = tp.tconst\
	WHERE ta.language = 'en';
  ```
  Use below command to review count of records from the denormalized view. You can foind approx 2.5 million records vs 47 million on the base table. At this point you source database is ready for migration to Amazon DynamoDB.
  ```bash
  select count(*) from dynamo_migration;
  ```
