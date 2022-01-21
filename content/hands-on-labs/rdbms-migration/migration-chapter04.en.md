+++
title = "Explore Target Model"
menuTitle = "Explore Target Model"
date = 2021-04-25T07:33:04-05:00
weight = 40

+++

Relational Database Management System (RDBMS) platforms store data in a normalized relational structure. This structure reduces hierarchical data structures and keeps data across multiple tables.
You can often query the data from multiple tables, and assemble at presentation layer. Though, that won't be effecient for ultra-low latency workload.
To support high-traffic queries with ultra-low latency, taking advantage of a NoSQL system generally makes technical and economic sense.

To start designing a target data model in Amazon DynamoDB that will scale efficiently, you must identify the common access patterns. For IMDb use case we have identified a set of access patterns as described below:
![Final Deployment Architecture](/images/migration32.png)

A common approach to DynamoDB schema design is to identify application layer entities and use denormalization and composite key aggregation to reduce query complexity.
In DynamoDB, this means using composite sort keys, overloaded global secondary indexes, partitioned tables/indexes, and other design patterns.
In this scenario, we will follow [Adjacency List Design Pattern](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-adjacency-graphs.html#bp-adjacency-lists), which is a common way to represent relational data structures in Amazon DynamoDB.
The advantages of this pattern includes optimal data duplication and simplified query patterns to find all metadata related to each movie.
The partition key in this model is tconst (unique movie id) and sort key is overloaded to define item type in the collection. Following prefix is used to indentify record type in the collection:

-	Multiple records prefixed with DETL contains cast/crew information per movie. There is 1: many relationships between title_basics and title_principals.
title_principals has all cast and crew information stored as separate rows per movie where as title_basics has movie metadata.
Information in both the tables are considered static once a movie is published. The access patterns required the movies and cast/crew information to be fetched together.
During target modelling, each cast/crew member (actor, director, producer etc.) metadata is denormalized with movie information and stored with sort key prefix DETL.
-	Multiple records prefixed with REGN contains all regions, languages and titles that a movie is published.
During target modelling the data is migrated as is to the DynamoDB table.
-	Multiple records prefixed with RTNG contains IMDb rating and number of votes. This is considered dynamic and frequent changing records for a movie.
In order to reduce I/O during update scenario, the record is not denormalized with other information in the the DynamoDB table.

![Final Deployment Architecture](/images/migration33.png)

A new GSI is created on the movies table with new partion key: nconst (unique per movie's crew) and sort key: movie start year. This will help to query access pattern by crew member (#6 inside the common access pattern table)

![Final Deployment Architecture](/images/migration34.png)

Below small video demonstrates how all of these access pattern are evaluated against target DynamoDB model.

<video width=100% controls autoplay>
    <source src="/images/migration36.mp4" type="video/mp4">
    Your browser does not support the video tag.
</video>
