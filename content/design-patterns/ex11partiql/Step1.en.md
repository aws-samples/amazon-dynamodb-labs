+++
title = "Step 1 - Create and load the the Gamers table"
date = 2019-12-02T12:24:33-08:00
weight = 1
+++


Run the AWS CLI command to create the table named `Gamers` and create a GSI named `GSI_1` which is partitioned on `SK` attribute of the parent table:

```bash
aws dynamodb create-table --table-name Gamers \
--attribute-definitions AttributeName=PK,AttributeType=S AttributeName=SK,AttributeType=S \
--key-schema AttributeName=PK,KeyType=HASH AttributeName=SK,KeyType=RANGE \
--provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5 \
--tags Key=workshop-design-patterns,Value=targeted-for-cleanup \
--global-secondary-indexes "IndexName=GSI_1,\
KeySchema=[{AttributeName=SK,KeyType=HASH},{AttributeName=PK,KeyType=RANGE}],\
Projection={ProjectionType=KEYS_ONLY},\
ProvisionedThroughput={ReadCapacityUnits=5,WriteCapacityUnits=5}"
```
Wait until the table becomes active:
```bash
aws dynamodb wait table-exists --table-name Gamers
```

Navigate to the DynamoDB section of the AWS management console.
In the left navigation pane, choose PartiQL editor. If you cannot see PartiQL, then you need to switch to new DynamoDB console.

![Amazon DynamoDB PartiQL editor](/images/awsconsolepartiQL.png)

Using PartiQL editor, run following insert statements to load items in `Gamers` table

`insert into Gamers value {'PK' : 'Hammer57','SK' : 'Assets','Coins': 1000}`

`insert into Gamers value {'PK' : 'Hammer57','SK' : 'Bank','Level': 87, 'Points' : 4050 , 'Tier' : 'Elite'}`

`insert into Gamers value {'PK' : 'Hammer57','SK' : 'Status','Health':'90%', 'Progress' : 30}`

`insert into Gamers value {'PK' : 'Hammer57','SK' : 'Weapon','Class' : 'Taser', 'Damage' : '55-67', 'Range' : 120}`

Next, write insert statement for a new gamer - Atom12 with 600 Coins and a second record for Atom12 with Health as 60%, Progress as 70?
