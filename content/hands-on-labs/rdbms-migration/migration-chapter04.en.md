+++
title = "Explore Target Model"
menuTitle = "Explore Target Model"
date = 2021-04-25T07:33:04-05:00
weight = 40

+++

Relational Database Management System (RDBMS) platforms store data in a normalized relational structure. This structure reduces hierarchical data structures and stores data across multiple tables.
You can often query the data from multiple tables and assemble at the presentation layer. However, that is not preferrable and won't be efficient for ultra-low read latency workloads.
To support high-traffic queries with ultra-low latency, designing a schema to take advantage of a NoSQL system generally makes technical and economic sense.

To start designing a target data model in Amazon DynamoDB that will scale efficiently, you must identify the common access patterns. For the IMDb use case we have identified a set of access patterns as described below:
![Final Deployment Architecture](/images/migration32.png)

A common approach to DynamoDB schema design is to identify application layer entities and use denormalization and composite key aggregation to reduce query complexity.
In DynamoDB, this means using [composite sort keys](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-sort-keys.html), [overloaded global secondary indexes](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-gsi-overloading.html), and other design patterns.


In this scenario, we will follow the [Adjacency List Design Pattern](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-adjacency-graphs.html#bp-adjacency-lists) with primary key overloading to store relational data in the DynamoDB table. The advantages of this pattern include optimal data duplication and simplified query patterns to find all metadata related to each movie. Normally the adjacency list pattern stores duplicate data under two items, each representing one half of the relationship. To associate a title with a region, for example, you would write one item for the region under the title and one item under the title under the region, like this:

| Partition Key        |  Sort Key           | Attribute List         |
| ------------- |:-------------:|:-------------:|
| tt0309377     | REGN\|NZ | ordering, language, region, title, types |
| REGN\|NZ      | tt0309377 | language, region, title  |

However in this lab we'll only work with one side of the relationship: the data residing under the title. Our partition key will be `mpkey` and our sort key `mskey` for the movies table. Each partition and sort key is prefixed with letters to identify the entity type, and the sort key uses `|` as a separator between the entity type and value.
The partition key is prefixed with `tt` (unique movie id) and sort key is overloaded to define the entity type.

The following entity types are found in the table:

- `tt`: A unique movie id. This is the entity type of the partition key in the base table
- `nm`: A unique entry for each movie crew member. This is the entity type of the GSI partition key
- `DETL`: Contains cast/crew information per movie. There is 1: many relationships between title_basics and title_principals.
title_principals has all cast and crew information stored as separate rows per movie where as title_basics has movie metadata.
Information in both the tables are considered static once a movie is published. The access patterns required the movies and cast/crew information to be fetched together.
During target modelling, each cast/crew member (actor, director, producer etc.) metadata is denormalized with movie information and stored with entity type `DETL`.
- `REGN`: Contains all regions, languages and titles that a movie is published.
During target modelling the data is migrated as is to the DynamoDB table.
- `RTNG`: Contains IMDb rating and number of votes. This is considered dynamic and frequent changing records for a movie.
In order to reduce I/O during update scenario, the record is not denormalized with other information in the the DynamoDB table.

![Final Deployment Architecture](/images/migration33.png)

A new GSI is created on the movies table with new partion key: `nconst` (unique per movie's crew with entity type `nm`) and sort key: `startYear`. This will help to query access pattern by crew member (#6 inside the common access pattern table)

![Final Deployment Architecture](/images/migration34.png)

Below small video demonstrates how all of these access pattern are evaluated against target DynamoDB model.

<video width=100% controls autoplay>
    <source src="https://www.amazondynamodblabs.com/static/rdbms-migration/migration36.mp4" type="video/mp4">
    Your browser does not support the video tag.
</video>
