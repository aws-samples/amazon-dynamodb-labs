---
title: "8. Cleanup"
date: 2021-04-21T07:33:04-05:00
weight: 80
description: "Delete the DynamoDB table and clean up resources."
---

::alert[If you are running this workshop in your own AWS account, complete this cleanup to avoid ongoing charges.]{type="warning"}

## Delete the CloudFormation stack

Because you provisioned the table with CloudFormation, you delete it by deleting the stack. CloudFormation removes the table and all its indexes:

```bash
aws cloudformation delete-stack --stack-name dynamodb-for-go-developers
```

Wait for the deletion to complete:

```bash
aws cloudformation wait stack-delete-complete --stack-name dynamodb-for-go-developers
```

Verify the table is gone:

```bash
aws dynamodb describe-table --table-name simple-inventory 2>&1
```

Expected output (after a few seconds):
```text
An error occurred (ResourceNotFoundException) when calling the DescribeTable operation: Requested resource not found: Table: simple-inventory not found
```

Letting CloudFormation own the full lifecycle - create and delete - is exactly the control-plane discipline you want in production. Your application code never creates or destroys infrastructure.

## If you used a workshop-provided environment

If you launched a VS Code environment via a separate CloudFormation stack during setup, delete that stack as well through the CloudFormation console or CLI.

## What you learned

You provisioned the table's infrastructure with **CloudFormation** (control plane) and used the AWS SDK for Go v2 only for **data-plane** operations:

| Operation | What it does | Module |
|-----------|-------------|--------|
| CloudFormation `AWS::DynamoDB::Table` | Provision table with GSIs and LSI | 2 |
| `PutItem` | Write a single item | 3 |
| `BatchWriteItem` | Write up to 25 items per call | 3 |
| `GetItem` | Read a single item by key | 4 |
| `Query` | Read items sharing a partition key | 4 |
| `Query` (GSI/LSI) | Secondary index lookups | 4 |
| `Scan` | Read the entire table | 4 |
| `UpdateItem` | Modify attributes with expressions | 5 |
| `DeleteItem` | Remove an item | 6 |
| `TransactWriteItems` | Atomic multi-item writes | 7 |
| `TransactGetItems` | Atomic multi-item reads | 7 |
| CloudFormation `delete-stack` | Tear down the table | 8 |

### Key design concepts applied

- **Control plane vs. data plane** - CloudFormation owns the table; the SDK handles items
- **Single table design** - multiple entity types in one table
- **Composite keys with prefixes** - `#USER#`, `#ORDER#`, `#ITEM#`
- **Inverted index GSI** - cross-partition lookups by sort key
- **Sparse index GSI** - only active items appear in the index
- **Local Secondary Index** - alternate sort order within a partition
- **Multi-attribute key GSI** - compose sort keys from multiple native attributes
- **Condition expressions** - optimistic locking and write guards
- **Transactions** - atomic operations across multiple items

### Next steps

- Explore [DynamoDB Best Practices](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/best-practices.html)
- Learn about [DynamoDB Streams](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Streams.html) for change data capture
- Try the [Advanced Design Patterns](/design-patterns) workshop for more complex modeling scenarios
