---
title: "Provision the table with CloudFormation"
date: 2021-04-21T07:33:04-05:00
weight: 20
---

In this step, you deploy the `simple-inventory` table and all its indexes. The CloudFormation template is already included in the project you cloned (`template.yaml`) - you review it here and then deploy it.

## Control plane vs. data plane

DynamoDB operations fall into two categories:

- **Control plane** - creating, updating, and deleting tables and indexes. These operations define your infrastructure.
- **Data plane** - reading and writing items (`PutItem`, `Query`, `UpdateItem`, and so on). These operations use your infrastructure.

In production, you manage the control plane with infrastructure-as-code (CloudFormation, CDK, or Terraform), not from application code. Your application uses the SDK only for the data plane. This separation gives you version-controlled, repeatable, reviewable infrastructure, and keeps table lifecycle decisions out of your request-handling code.

For that reason, you provision the table with CloudFormation here. The Go code you write in later modules only reads and writes items.

## The CloudFormation template

Open `template.yaml` in the project you cloned and read through it:

```yaml
AWSTemplateFormatVersion: "2010-09-09"
Description: DynamoDB single table for the DynamoDB for Go Developers workshop

Resources:
  InventoryTable:
    Type: AWS::DynamoDB::Table
    Properties:
      TableName: simple-inventory
      BillingMode: PAY_PER_REQUEST
      AttributeDefinitions:
        - AttributeName: pk
          AttributeType: S
        - AttributeName: sk
          AttributeType: S
        - AttributeName: placed_id
          AttributeType: S
        - AttributeName: status_date
          AttributeType: S
        - AttributeName: status
          AttributeType: S
        - AttributeName: created_at
          AttributeType: S
      KeySchema:
        - AttributeName: pk
          KeyType: HASH
        - AttributeName: sk
          KeyType: RANGE
      GlobalSecondaryIndexes:
        - IndexName: inverted-index
          KeySchema:
            - AttributeName: sk
              KeyType: HASH
            - AttributeName: pk
              KeyType: RANGE
          Projection:
            ProjectionType: ALL
        - IndexName: placed-index
          KeySchema:
            - AttributeName: placed_id
              KeyType: HASH
          Projection:
            ProjectionType: ALL
        - IndexName: status-date-gsi
          KeySchema:
            - AttributeName: pk
              KeyType: HASH
            - AttributeName: status
              KeyType: RANGE
            - AttributeName: created_at
              KeyType: RANGE
          Projection:
            ProjectionType: ALL
      LocalSecondaryIndexes:
        - IndexName: status-date-index
          KeySchema:
            - AttributeName: pk
              KeyType: HASH
            - AttributeName: status_date
              KeyType: RANGE
          Projection:
            ProjectionType: ALL

Outputs:
  TableName:
    Description: Name of the DynamoDB table
    Value: !Ref InventoryTable
  TableArn:
    Description: ARN of the DynamoDB table
    Value: !GetAtt InventoryTable.Arn
```

## Walking through the template

**`AttributeDefinitions`** declares only the attributes used in a key schema - the table's primary key plus every index key. You declare six here: `pk`, `sk`, `placed_id`, `status_date`, `status`, and `created_at`. Non-key attributes (`email`, `full_name`, `price`, and so on) are never declared; DynamoDB is schemaless beyond the keys.

**`KeySchema`** defines the primary key: `pk` (HASH / partition key) and `sk` (RANGE / sort key). Together they uniquely identify every item.

**`inverted-index` GSI** swaps the keys - `sk` becomes the partition key and `pk` the sort key - so you can find an item by its sort key value across all partitions.

**`placed-index` GSI** uses `placed_id` as its partition key. Because only pending and confirmed orders carry a `placed_id` attribute, this is a sparse index: only those items appear in it.

**`status-date-gsi` GSI** uses **multi-attribute keys** - a newer DynamoDB feature. Its sort key is composed of two independent attributes: `status` and `created_at`. Notice the `KeySchema` lists one `HASH` entry and *two* `RANGE` entries. This is the modern alternative to the concatenated `status_date` string used by the LSI below. You use this index in Module 4.

**`status-date-index` LSI** shares the base table's partition key (`pk`) and uses the concatenated `status_date` string as its sort key. LSIs must be defined at table creation time and share the table's partition key.

**`BillingMode: PAY_PER_REQUEST`** is on-demand billing - you pay per request with no capacity planning.

::alert[Multi-attribute keys are a GSI-only feature: a GSI sort key can be composed of up to four attributes. LSIs and the base table key schema still use a single sort key attribute.]{type="info"}

## Deploy the stack

Deploy the template with the AWS CLI:

```bash
aws cloudformation deploy \
  --template-file template.yaml \
  --stack-name dynamodb-for-go-developers
```

Expected output:
```text
Waiting for changeset to be created..
Waiting for stack create/update to complete
Successfully created/updated stack - dynamodb-for-go-developers
```

## Verify the table

Confirm the table is active:

```bash
aws dynamodb describe-table --table-name simple-inventory --query "Table.TableStatus"
```

Expected output:
```text
"ACTIVE"
```

Confirm the indexes were created:

```bash
aws dynamodb describe-table --table-name simple-inventory \
  --query "Table.[GlobalSecondaryIndexes[].IndexName, LocalSecondaryIndexes[].IndexName]"
```

Expected output:
```json
[
    ["inverted-index", "placed-index", "status-date-gsi"],
    ["status-date-index"]
]
```

Your table is ready. Because CloudFormation owns the table's lifecycle, you never create or delete it from application code. In the next module, you start writing data to it with the Go SDK.
