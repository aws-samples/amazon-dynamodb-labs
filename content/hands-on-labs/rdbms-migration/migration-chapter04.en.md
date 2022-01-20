+++
title = "Explore Target Model"
menuTitle = "Explore Target Model"
date = 2021-04-25T07:33:04-05:00
weight = 40

+++

Relational Database Management System (RDBMS) platforms store data in a normalized relational structure. This structure reduces hierarchical data structures and keeps data across multiple tables.
You can often query the data from multiple tables, and assemble at presentation layer. Though, for ultra-low latency response to high-traffic queries, taking advantage of a NoSQL system generally makes technical and economic sense.
You can always perform lift and shift migration from relational databases to DynamoDB using Database Migration Service.

To start designing a DynamoDB table that will scale efficiently, you must identify the access patterns. For IMDb use case we have identified following access patterns:
![Final Deployment Architecture](/images/migration32.png)

A common approach to DynamoDB schema design is to identify application layer entities and use denormalization and composite key aggregation to reduce query complexity.
In DynamoDB, this means using composite sort keys, overloaded global secondary indexes, partitioned tables/indexes, and other design patterns.
In this scenario, we will follow [Adjacency List Design Pattern](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-adjacency-graphs.html#bp-adjacency-lists), which is a common way to represent relational data structures in DynamoDB.
The advantages of this pattern include minimal data duplication and simplified query patterns to find all metadata related to each movie.
The partition key in this model is tconst (unique movie id) and sort key defines the type of record in the collection. Items has sort key starts with:
	1.	DETL contains movies related metadata information (mostly static at the time of publication)
	2.	REGN contains multiple records, each with single region, language and movie title
	3.	RTNG contains IMDb rating and number of votes. This information is stores as separate record since the information is dynamic and frequently updates over time. This will help to reduce I/O operation during update.

![Final Deployment Architecture](/images/migration33.png)

GSI is created on the movies table with new partion key: nconst (unique per movie's crew) and sort key: movie start year. This will help to query access pattern by crew member (#6 inside the common access pattern table)

![Final Deployment Architecture](/images/migration34.png)

Below video demonstrates how access pattern are evaluated against the DynamoDB model.

<video width=100% controls autoplay>
    <source src="/images/migration36.mp4" type="video/mp4">
    Your browser does not support the video tag.
</video>
