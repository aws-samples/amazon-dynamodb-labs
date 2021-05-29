+++
title = "Read Sample Data"
date = 2020-04-21T07:38:58-05:00
weight = 21
+++

Before we can do anything we have to learn what our data looks like.

DynamoDB provides the [Scan API](https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_Scan.html) which can be invoked using the [scan CLI command](https://docs.aws.amazon.com/cli/latest/reference/dynamodb/scan.html). Scan will do a full table scan and return the items in 1MB chunks.  Scanning is the slowest and most expensive way to get data out of DynamoDB; Scanning this on a large table from the CLI might be unwieldy but we know there are only a few items in our sample data so its OK to do here.  Try running a scan on the ProductCatalog table:

```bash
aws dynamodb scan --table-name ProductCatalog
```

Data input and output in the CLI utilizes the DynamoDB JSON format, which is described in the [DynamoDB Low-Level API](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Programming.LowLevelAPI.html) section of the Developer Guide.

We can see from our data that this ProductCatalog table has two types of products: Book and Bicyle items.

If we wanted to read just a single item, we would use the [GetItem API](https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_GetItem.html) which can be invoked using the [get-item CLI command](https://docs.aws.amazon.com/cli/latest/reference/dynamodb/get-item.html). GetItem is the fastest and cheapest way to get data out of DynamoDB as you must specify the full Primary Key so the command is guaranteed to match at most one item in the table.

```bash
aws dynamodb get-item \
    --table-name ProductCatalog \
    --key '{"Id":{"N":"101"}}'
```

By default a read from DynamoDB will use *eventual consistency* because eventually consistent reads in DynamoDB are half the price of a *strongly consistent* read.  See [Read Consistency](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.ReadConsistency.html) in the DynamoDB Developer Guide for more information.

There are many useful options to the get-item command but a few that get used regularly are:

* *\-\-consistent-read* : Specifying that you want a strongly consistent read
* *\-\-projection-expression* : Specifying that you only want certain attributes returned in the request
* *\-\-return-consume-capacity* : Tell us how much capacity was consumed by the request

Let's run the previous command and add some of these options to the command line:

```bash
aws dynamodb get-item \
    --table-name ProductCatalog \
    --key '{"Id":{"N":"101"}}' \
    --consistent-read \
    --projection-expression "ProductCategory, Price, Title" \
    --return-consumed-capacity TOTAL
```

We can see from the returned values:

```json
{
    "Item": {
        "Price": {
            "N": "2"
        },
        "Title": {
            "S": "Book 101 Title"
        },
        "ProductCategory": {
            "S": "Book"
        }
    },
    "ConsumedCapacity": {
        "TableName": "ProductCatalog",
        "CapacityUnits": 1.0
    }
}
```

That performing this request consume 1.0 RCU, because this item is less than 4KB.  If we run the command again but remove the *\-\-consistent-read* option, we will see that eventually consistent reads consume half as much capacity:

```bash
aws dynamodb get-item \
    --table-name ProductCatalog \
    --key '{"Id":{"N":"101"}}' \
    --projection-expression "ProductCategory, Price, Title" \
    --return-consumed-capacity TOTAL
```

We will see this output:

```
{
    "Item": {
        "Price": {
            "N": "2"
        },
        "Title": {
            "S": "Book 101 Title"
        },
        "ProductCategory": {
            "S": "Book"
        }
    },
    "ConsumedCapacity": {
        "TableName": "ProductCatalog",
        "CapacityUnits": 0.5
    }
}
```
