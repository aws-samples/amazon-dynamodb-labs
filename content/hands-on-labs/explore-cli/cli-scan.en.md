+++
title = "Working with Table Scans"
date = 2020-04-21T07:38:58-05:00
weight = 23
+++

As mentioned previously, the [Scan API](https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_Scan.html) which can be invoked using the [scan CLI command](https://docs.aws.amazon.com/cli/latest/reference/dynamodb/scan.html). Scan will do a full table scan and return the items in 1MB chunks.

The Scan API is similar to the Query API except that since we want to scan the whole table and not just a single Item Collection, there is no Key Condition Expression for a Scan.  However, you can specify a [Filter Expression](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Scan.html#Scan.FilterExpression) which will reduce the size of the result set (even though it will not reduce the amount of capacity consumed).

For example, we could find all the replies in the Reply that were posted by User A:

```bash
aws dynamodb scan \
    --table-name Reply \
    --filter-expression 'PostedBy = :user' \
    --expression-attribute-values '{
        ":user" : {"S": "User A"}
    }' \
    --return-consumed-capacity TOTAL
```

Note than in the response we see these lines:

```
"Count": 3,
"ScannedCount": 4,
```

This is telling us that the Scan scanned all 4 items (ScannedCount) in the table and thats what we were charged to read, but the Filter Expression reduced our result set size down to 3 items (Count).

Sometimes when scanning data there will be more data than will fit in the response if the scan hits the 1MB limit on the server side, or there may be more items left than our specified *\-\-max-items* parameter.  In that case, the scan response will include a *NextToken* which we can then issue to a subsequent scan call to pick up where we left off.  For example in the previous scan we know that 3 items were in the result set.  Let's run it again but limit the max items to 2:

```bash
aws dynamodb scan \
    --table-name Reply \
    --filter-expression 'PostedBy = :user' \
    --expression-attribute-values '{
        ":user" : {"S": "User A"}
    }' \
    --max-items 2 \
    --return-consumed-capacity TOTAL
```
We can see in the response that there is a

```text
"NextToken": "eyJFeGNsdXNpdmVTdGFydEtleSI6IG51bGwsICJib3RvX3RydW5jYXRlX2Ftb3VudCI6IDJ9"
```

So we can invoke the scan request again, this time passing that NextToken value into the *\-\-starting\-token* parameter:

```bash
aws dynamodb scan \
    --table-name Reply \
    --filter-expression 'PostedBy = :user' \
    --expression-attribute-values '{
        ":user" : {"S": "User A"}
    }' \
    --max-items 2 \
    --starting-token eyJFeGNsdXNpdmVTdGFydEtleSI6IG51bGwsICJib3RvX3RydW5jYXRlX2Ftb3VudCI6IDJ9 \
    --return-consumed-capacity TOTAL
```

## Exercise

Explore the data in the *Forum* table and write a scan command to return only the Forums that have more than 1 thread and more than 50 views.

Hint: Read about [Reserved Words](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/ReservedWords.html) in DynamoDB and how to deal with [situations where one of your attribute names is a reserved word](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Expressions.ExpressionAttributeNames.html).

The solution is expandable below but try to figure it out yourself before moving forward.

**Click below to expand and see the exercise solutions**

{{%expand "Expand this to see the solution" %}}
First we need to understand the structure of the data in the Forum Table so let's do a scan to see what attributes exist:

```bash
aws dynamodb scan \
    --table-name Forum
```

```json
{
    "Count": 2,
    "Items": [
        {
            "Category": {
                "S": "Amazon Web Services"
            },
            "Name": {
                "S": "Amazon S3"
            }
        },
        {
            "Category": {
                "S": "Amazon Web Services"
            },
            "Threads": {
                "N": "2"
            },
            "Messages": {
                "N": "4"
            },
            "Name": {
                "S": "Amazon DynamoDB"
            },
            "Views": {
                "N": "1000"
            }
        }
    ],
    "ScannedCount": 2,
    "ConsumedCapacity": null
}
```

We can see that some items have a `Threads` number attribute and a `Views` number attribute. To solve this problem we want to use those attributes in our FilterExpression.  Make sure to specify that these values are of the Number type by using "N" in the *\-\-expression\-attribute\-values* parameter.

```bash
aws dynamodb scan \
    --table-name Forum \
    --filter-expression 'Threads >= :threads AND Views >= :views' \
    --expression-attribute-values '{
        ":threads" : {"N": "1"},
        ":views" : {"N": "50"}
    }' \
    --return-consumed-capacity TOTAL
```

When you run this command you receive the following error:

```text
An error occurred (ValidationException) when calling the Scan operation: Invalid FilterExpression: Attribute name is a reserved keyword; reserved keyword: Views
```

That's because the *Views* attribute name is actually a [DynamoDB Reserved Word](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/ReservedWords.html).  DynamoDB gives us the ability to put a placeholder in the FilterExpression and provide the actual attribute name in the *\-\-expression\-attribute\-names* CLI parameter.  For more information please see the [Expression Attribute Names in DynamoDB](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Expressions.ExpressionAttributeNames.html) in the Developer Guide.

To solve our problem here:

```bash
aws dynamodb scan \
    --table-name Forum \
    --filter-expression 'Threads >= :threads AND #Views >= :views' \
    --expression-attribute-values '{
        ":threads" : {"N": "1"},
        ":views" : {"N": "50"}
    }' \
    --expression-attribute-names '{"#Views" : "Views"}' \
    --return-consumed-capacity TOTAL
```

{{% /expand%}}
