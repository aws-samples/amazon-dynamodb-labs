+++
title = "Step 2 - Create and load the the Gamers table"
date = 2019-12-02T12:24:33-08:00
weight = 1
+++

Insert statement for loading data for second Gamer - Atom12

`insert into Gamers value {'PK' : 'Atom12','SK' : 'Assets','Coins': 600}`

`insert into Gamers value {'PK' : 'Atom12','SK' : 'Status','Health':'60%', 'Progress' : 70}`

Use below UPDATE statement to modify `Health` for an item. Where condition in `update` must resolve to a single primary key value.

`update Gamers
set Health = '100%'
where PK='Hammer57' and SK='Status'
`

What happens if the WHERE clause of the UPDATE statement does not evaluate to true? Give it a try by changing above update with `PK = 'Hammer58' and SK='Status'`

Let's decrement coins by 400 for bumping up health to 100%. We will use subtract operator `-`.

`update Gamers
set Coins=Coins - 400
where PK='Hammer57' and SK='Assets'
`

We can view the changes in Coins and Health using `select` statement.

`select * from Gamers where PK='Hammer57'`

In real word scenario, above 2 updates should happen simultaneously. Both should either succeed or fail. This can be done using Transactions. Also, we can add a `ConditionCheck` to check if Gamer has enough Coins to buy health.


We will see in next section how to use transactions with PartiQL for DynamoDB.
