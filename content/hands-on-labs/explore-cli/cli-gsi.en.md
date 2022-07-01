+++
title = "Global Secondary Indexes"
date = 2021-04-24T07:38:58-05:00
weight = 27
+++

We have concerned ourself hitherto with accessing data based on the key attributes. If we wanted to look for items based on non-key attributes we had to do a full table scan and use filter conditions to find what we wanted, which would be both very slow and very expensive for systems operating at large scale.

DynamoDB provides a feature called [Global Secondary Indexes (GSIs)](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GSI.html) which will automatically pivot your data around different Partition and Sort Keys. Data can be re-grouped and re-sorted to allow for more access patterns to be quickly served with the Query and Scan APIs.

Remember the previous example where we wanted to find all the replies in the **Reply** table that were posted by User A:

```bash
aws dynamodb scan \
    --table-name Reply \
    --filter-expression 'PostedBy = :user' \
    --expression-attribute-values '{
        ":user" : {"S": "User A"}
    }' \
    --return-consumed-capacity TOTAL
```

When running that scan operation we could see that the *Count* returned was different than the *ScannedCount*.  If there had been a billion Reply items but only three of them were posted by User A, we would have to pay (both in time and money) to scan through a billion items just to find the three we wanted.

Armed with this knowledge of GSIs, we can now create a GSI on the **Reply** table to service this new access pattern.  GSIs can be created and removed at any time, even if the table has data in it already! This new GSI will use the *PostedBy* attribute as the Partition (HASH) key and we will still keep the messages sorted by *ReplyDateTime* as the Sort (RANGE) key.  We want all the attributes from the table copied (projected) into the GSI so we will use the ALL ProjectionType.  Note that the name of the index we create is `PostedBy-ReplyDateTime-gsi`.

```bash
aws dynamodb update-table \
    --table-name Reply \
    --attribute-definitions AttributeName=PostedBy,AttributeType=S AttributeName=ReplyDateTime,AttributeType=S \
    --global-secondary-index-updates '[{
        "Create":{
            "IndexName": "PostedBy-ReplyDateTime-gsi",
            "KeySchema": [
                {
                    "AttributeName" : "PostedBy",
                    "KeyType": "HASH"
                },
                {
                    "AttributeName" : "ReplyDateTime",
                    "KeyType" : "RANGE"
                }
            ],
            "ProvisionedThroughput": {
                "ReadCapacityUnits": 5, "WriteCapacityUnits": 5
            },
            "Projection": {
                "ProjectionType": "ALL"
            }
        }
    }
]'
```

It can take a little time while DynamoDB creates the GSI and backfills data from the table into the index.  We can watch this from the command line and wait until the IndexStatus goes `ACTIVE`:

```bash
aws dynamodb describe-table --table-name Reply | grep IndexStatus
```

Once the GSI has become `ACTIVE`, continue on to the exercise below.

## Exercise

1. Find all the Replies written by User A sorted, using the query command instead of the scan command.

Hint: When using a GSI in DynamoDB you have to explicitly tell DynamoDB both the table name and the index name.

2. Try running a `get-item` command against the GSI.  Why doesn't this work?

The solution is expandable below but try to figure it out yourself before moving forward.

**Click below to expand and see the exercise solutions**

{{%expand "Expand this to see the solution" %}}

1. Running a `query` on a GSI is no different than running it against a table, except we also need to specify which GSI to use with the *\-\-index\-name* option and we'll use the GSI key attributes in the KeyConditionExpression.

```bash
aws dynamodb query \
    --table-name Reply \
    --key-condition-expression 'PostedBy = :pb' \
    --expression-attribute-values '{
        ":pb" : {"S": "User A"}
    }' \
    --index-name PostedBy-ReplyDateTime-gsi \
    --return-consumed-capacity TOTAL
```

Note that in the output:

```bash
"Count": 3,
"ScannedCount": 3,
```

The `query` could not be more optimal than this.  Even if the table has a billion **Reply** items authored by other Users, this query will only cost us to read the exact 3 items we're hoping to return (unlike a `scan`).

2. In the base table, the Primary Key uniquely identifies the row which means that a `get-item` request will match AT MOST one item. Since we can select any attributes as the Keys for a GSI, there is no guarantee that the keys of a GSI will uniquely identify a single item. Therefore, DynamoDB prevents you from executing a `get-item` against a GSI.

{{% /expand%}}

### Cleanup

When you're done, make sure to remove the GSI.

```bash
aws dynamodb update-table \
    --table-name Reply \
    --global-secondary-index-updates '[{
        "Delete":{
            "IndexName": "PostedBy-ReplyDateTime-gsi"
        }
    }
]'
```
