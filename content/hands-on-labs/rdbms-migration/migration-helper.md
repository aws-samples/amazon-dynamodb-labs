mysql -u root -pPassword@123
# 1. Create new IMDB Database
CREATE DATABASE imdb;
USE imdb;
# 2. Create new tables with primary key - Move this to the UserData section
CREATE TABLE title_akas (titleId VARCHAR(200), ordering VARCHAR(200),title VARCHAR(1000), region VARCHAR(1000), language VARCHAR(1000), types VARCHAR(1000),attributes VARCHAR(1000),isOriginalTitle VARCHAR(5),primary key (titleId, ordering));
CREATE TABLE imdb.title_basics (tconst  VARCHAR(200), titleType  VARCHAR(1000),primaryTitle  VARCHAR(1000), originalTitle  VARCHAR(1000), isAdult  VARCHAR(1000), startYear  VARCHAR(1000),endYear  VARCHAR(1000),runtimeMinutes  VARCHAR(1000),genres  VARCHAR(1000),primary key (tconst));
CREATE TABLE title_crew (tconst  VARCHAR(200), directors  VARCHAR(1000),writers  VARCHAR(1000),primary key (tconst));
CREATE TABLE title_episode (tconst  VARCHAR(200), parentTconst  VARCHAR(1000),seasonNumber  integer, episodeNumber  integer,primary key (tconst));
CREATE TABLE title_principals (tconst  VARCHAR(200), ordering  VARCHAR(200),nconst  VARCHAR(200), category  VARCHAR(1000), job  VARCHAR(1000), characters  VARCHAR(1000),primary key (tconst,ordering,nconst));
CREATE TABLE title_ratings (tconst  VARCHAR(200), averageRating float,numVotes  integer,primary key (tconst));
CREATE TABLE name_basics (nconst  VARCHAR(200), primaryName  VARCHAR(1000),birthYear  VARCHAR(1000), deathYear  VARCHAR(1000), primaryProfession  VARCHAR(1000), knownForTitles VARCHAR(1000),primary key (nconst));
# 3. Load data into tables - Move this to the UserData section
LOAD DATA INFILE '/var/lib/mysql-files/title.ratings.tsv' IGNORE INTO TABLE imdb.title_ratings FIELDS TERMINATED BY '\t'  IGNORE 1 LINES;
LOAD DATA INFILE '/var/lib/mysql-files/title.basics.tsv'  IGNORE INTO TABLE imdb.title_basics FIELDS TERMINATED BY '\t'  IGNORE 1 LINES;
LOAD DATA INFILE '/var/lib/mysql-files/title.crew.tsv' IGNORE INTO TABLE imdb.title_crew FIELDS TERMINATED BY '\t'  IGNORE 1 LINES;
LOAD DATA INFILE '/var/lib/mysql-files/title.episode.tsv' IGNORE INTO TABLE imdb.title_episode FIELDS TERMINATED BY '\t'  IGNORE 1 LINES;
LOAD DATA INFILE '/var/lib/mysql-files/title.principals.tsv' IGNORE INTO TABLE imdb.title_principals FIELDS TERMINATED BY '\t'  IGNORE 1 LINES; # This table is partially loaded
LOAD DATA INFILE '/var/lib/mysql-files/name.basics.tsv' IGNORE INTO TABLE imdb.name_basics FIELDS TERMINATED BY '\t'  IGNORE 1 LINES;
LOAD DATA INFILE '/var/lib/mysql-files/title.akas.tsv' IGNORE INTO  TABLE imdb.title_akas FIELDS TERMINATED BY '\t'  IGNORE 1 LINES;
# 4. Create view and to limit the result set, filter the dataset with US region and English language
CREATE VIEW dynamo_migration AS \
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
	LEFT JOIN imdb.title_ratings tr ON tr.tconst = tp.tconst;\
	LEFT JOIN imdb.title_akas ta ON ta.titleId = tp.tconst\
	WHERE ta.region = 'US' and ta.language = 'en';
#DMS Migration rule (Check if Source View has all the Key fields avaiable)
{
    "rules": [
        {
            "rule-type": "selection",
            "rule-id": "1",
            "rule-name": "1",
            "object-locator": {
                "schema-name": "imdb",
                "table-name": "dynamo_migration",
                "table-type": "view"
            },
            "rule-action": "include"
        },
        {
            "rule-type": "object-mapping",
            "rule-id": "2",
            "rule-name": "2",
            "rule-action": "map-record-to-record",
            "object-locator": {
                "schema-name": "imdb",
                "table-name": "dynamo_migration",
                "table-type": "view"
            },
            "target-table-name": "dynamo_migration",
            "mapping-parameters": {
                "partition-key-name": "tconst",
                "sort-key-name": "tconst_orderning",
                "exclude-columns": [],
                "attribute-mappings": [
                    {
                        "target-attribute-name": "tconst",
                        "attribute-type": "scalar",
                        "attribute-sub-type": "string",
                        "value": "${tconst}"
                    },
                    {
                        "target-attribute-name": "tconst_orderning",
                        "attribute-type": "scalar",
                        "attribute-sub-type": "string",
                        "value": "${category}|${nconst}|${ordering}"
                    }
                ]
            }
        }
    ]
}
#Create DynamoDB table with tconst (String) as partition key and tconst_orderning (String) as Sort key
