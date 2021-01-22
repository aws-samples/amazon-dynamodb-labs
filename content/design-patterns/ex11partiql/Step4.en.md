+++
title = "Step 4 - Running Batch Operations with PartiQL for DynamoDB"
date = 2019-12-02T12:24:33-08:00
weight = 1
+++

### Running Batch Operations with PartiQL for DynamoDB

This section shows how to perform batch writes on data stored in DynamoDB, using PartiQL.

In batch operation, entire operation must consist of either read statements or write statements; you cannot mix both in one batch.

We will add data for new Gamer - `Saber9` as part of a Batch operation.

The individual insert specified in Batch are atomic; however entire batch operation as a whole is not. We will see this in action by introducing an error in one of the insert statement as part of a batch.

Below is the batch statement. Notice in last insert statement Sort key is empty. Partition key and sort key attributes of base tables require to be non-empty values. So last insert statement in this batch will fail but others will succeed.

```
[
    {
        "Statement": "INSERT INTO Gamers value {'PK':'Saber9','SK':'Assets','Coins':2000}"
    },
   {
        "Statement": "INSERT INTO Gamers value {'PK':'Saber9','SK':'Bank','Level':98,'Points':6000,'Tier':'Elite'}"
   },
   {
        "Statement": "INSERT INTO Gamers value {'PK':'Saber9','SK':'Games','Genre':{'Action':['Halo','Call Of Duty'], 'Sports':['NBA','NHL']}}"
   },
   {
        "Statement": "INSERT INTO Gamers value {'PK':'Saber9','SK':''}"
   }
]
```

Let's execute below statement.

`aws dynamodb batch-execute-statement  --statements  file://partiql_batch.json`

The response will show success for 3 insert statement and last failed with ValidationError. This is expected as Sort key is empty.

In `select` statement, we can also get members of map data type. `Genre` is a map attribute in Gamers table. Run following command in PartiQL editor to select `Sports` from Genre attribute. 

`select PK, SK, Genre.Sports from Gamers where PK='Saber9'`

This concludes Amazon DynamoDB PartiQL module.
