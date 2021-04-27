+++
title = "Working with Table Scans"
date = 2020-04-21T07:38:58-05:00
weight = 23
+++

As mentioned previously, the [Scan API](https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_Scan.html) which can be invoked using the [scan CLI command](https://docs.aws.amazon.com/cli/latest/reference/dynamodb/scan.html). Scan will do a full table scan and return the items in 1MB chunks.

The Scan API is similar to the Query API except that since we want to scan the whole table and not just a single Item Collection, there is no Key Condition Expression for a Scan.  However, you can specify a [Filter Expression](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Scan.html#Scan.FilterExpression) which will reduce the size of the result set (even though it will not reduce the amount of capacity consumed).

For example, we could find all the replies in the Reply that were posted by User A:

    aws dynamodb scan \
        --table-name Reply \
        --filter-expression 'PostedBy = :user' \
        --expression-attribute-values '{
            ":user" : {"S": "User A"}
        }' \
        --return-consumed-capacity TOTAL

Note than in the response we see these lines:

    "Count": 3,
    "ScannedCount": 4,

This is telling us that the Scan scanned all 4 items (ScannedCount) in the table and thats what we were charged to read, but the Filter Expression reduced our result set size down to 3 items (Count).



Sometimes when scanning data there will be more data than will fit in the response if the scan hits the 1MB limit on the server side, or there may be more items left than our specified **\-\-max-items** parameter.  In that case, the scan response will include a **NextToken** which we can then issue to a subsequent scan call to pick up where we left off.  For example in the previous scan we know that 3 items were in the result set.  Let's run it again but limit the max items to 2:

    aws dynamodb scan \
        --table-name Reply \
        --filter-expression 'PostedBy = :user' \
        --expression-attribute-values '{
            ":user" : {"S": "User A"}
        }' \
        --max-items 2 \
        --return-consumed-capacity TOTAL

We can see in the response that there is a

    "NextToken": "eyJFeGNsdXNpdmVTdGFydEtleSI6IG51bGwsICJib3RvX3RydW5jYXRlX2Ftb3VudCI6IDJ9"

So we can invoke the scan request again,

Sometimes when scanning data there will be more data than will fit in the response if the scan hits the 1MB limit on the server side.  In that case, the scan response will include a *LastEvaluatedKey* which we can then issue to a subsequent scan call to pick up where we left off by passing the previously returned LastEvaluatedKey in using the  .  For example in the previous scan we know that 3 items were in the result set.  Let's run it again but limit the max items to 2:

**Exercise**

Explore the data in the **Forum** table and write a scan command to return only the Forums that have more than 1 thread and more than 50 views.


Hint: consider the *page-size* and *scan-index-forward* options.  The solution is on the next page but try to figure it out yourself before moving forward.
