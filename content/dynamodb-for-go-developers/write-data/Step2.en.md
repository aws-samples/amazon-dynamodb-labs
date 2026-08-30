---
title: "BatchWriteItem - Bulk load data"
date: 2021-04-21T07:33:04-05:00
weight: 20
---

The `BatchWriteItem` operation lets you write up to 25 items in a single API call. This is more efficient than calling `PutItem` repeatedly when you need to load multiple items.

In this step, you implement the bulk-load path and load the sample data you use for the rest of the workshop.

## Your turn: implement BatchWriteItems

Find the `BatchWriteItems` stub in `repository.go` and complete it, following the `TODO(lab)` comment. Two patterns matter here:

1. **Chunking into batches of 25** - DynamoDB limits `BatchWriteItem` to 25 items per request, so process the input slice in chunks of at most 25.

2. **Retrying unprocessed items** - if DynamoDB cannot process all items (due to throughput limits), it returns them in `UnprocessedItems`. Retry until all items are written. In a production application, you would add exponential backoff to this retry loop.

For the API shape (the `RequestItems` map, `WriteRequest` / `PutRequest`, and the `UnprocessedItems` returned in the response), see the AWS documentation:

- [BatchWriteItem API reference](https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_BatchWriteItem.html)
- [Go SDK v2: Client.BatchWriteItem](https://pkg.go.dev/github.com/aws/aws-sdk-go-v2/service/dynamodb#Client.BatchWriteItem)

::::expand{header="Expand this to see the solution for BatchWriteItems"}
```go
func (r *Repository) BatchWriteItems(ctx context.Context, items []map[string]types.AttributeValue) error {
	for i := 0; i < len(items); i += 25 {
		end := i + 25
		if end > len(items) {
			end = len(items)
		}

		batch := items[i:end]
		var writeRequests []types.WriteRequest
		for _, item := range batch {
			writeRequests = append(writeRequests, types.WriteRequest{
				PutRequest: &types.PutRequest{Item: item},
			})
		}

		output, err := r.client.BatchWriteItem(ctx, &dynamodb.BatchWriteItemInput{
			RequestItems: map[string][]types.WriteRequest{
				r.tableName: writeRequests,
			},
		})
		if err != nil {
			return err
		}

		for len(output.UnprocessedItems) > 0 {
			output, err = r.client.BatchWriteItem(ctx, &dynamodb.BatchWriteItemInput{
				RequestItems: output.UnprocessedItems,
			})
			if err != nil {
				return err
			}
		}
	}
	return nil
}
```
::::

## SeedData is provided for you

The project's demo harness (`demo.go`) builds the sample dataset as typed model objects - three users, six orders in various states, and six order items - and exposes a `load-data` command that calls `SeedData`. `SeedData` itself is **already implemented** in `repository.go`, because it is plain Go plumbing rather than a DynamoDB concept: it loops over the models, marshals each one with the helpers you wrote (`marshalUser`, `marshalOrder`, `marshalOrderItem`), and hands the combined slice to your `BatchWriteItems`.

You do not need to change it. Once your `marshalOrder`, `marshalOrderItem`, and `BatchWriteItems` implementations are in place, `SeedData` works as-is.

::alert[The `BatchWriteItems` stub's `// TODO(lab):` comment describes the exact structure. If you get stuck, see the full reference solution as described in :link[Set up the Go project]{href="/dynamodb-for-go-developers/setup/step1"}.]{type="info"}

## Run the bulk load

```bash
go run . load-data
```

Expected output:
```text
Loading sample data...
Successfully loaded 15 items.
```

If you instead see a `TODO(lab): ... not implemented` error, the message names the function still missing an implementation - fill it in and re-run.

## Verify the data

Count the items in the table:

```bash
aws dynamodb scan --table-name simple-inventory --select COUNT
```

Expected output:
```json
{
    "Count": 15,
    "ScannedCount": 15,
    "ConsumedCapacity": null
}
```

You should see a count that includes all users, orders, and order items you loaded.

You now have sample data in the table that supports all the query patterns you explore in the next modules.
