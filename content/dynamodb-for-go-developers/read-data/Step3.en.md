---
title: "Scan and parallel scan"
date: 2021-04-21T07:33:04-05:00
weight: 30
---

The `Scan` operation reads every item in the table (or index). Unlike `Query`, which targets a specific partition, `Scan` examines every item and returns those that match an optional filter expression.

## When to use Scan

Scan is appropriate for:
- **Analytics** - aggregating data across the entire table
- **Migrations** - reading all items to transform or move them
- **Small tables** - when the table has few items
- **Administrative tools** - export, backup, or reporting

Scan is **not** appropriate for normal application queries. It reads every item in the table, consuming capacity proportional to the entire table size, even if a filter discards most items. When you need a recurring query for items with a known attribute value - for example "all pending orders" - a **sparse index** is the right tool, not a filtered scan. You already built one: the sparse `placed-index` GSI, which `GetPendingOrders` queried in the previous step reads only the pending/confirmed orders directly, instead of scanning the whole table and discarding the rest.

Reference documentation for the exercises in this step:

- [Working with scans in DynamoDB](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Scan.html)
- [Paginating the results](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Scan.html#Scan.Pagination)
- [Parallel scan](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Scan.html#Scan.ParallelScan)
- [Filter expressions for scan](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Scan.html#Scan.FilterExpression)
- [Go SDK v2: NewScanPaginator](https://pkg.go.dev/github.com/aws/aws-sdk-go-v2/service/dynamodb#NewScanPaginator)

## Your turn: basic scan with pagination

The Go SDK provides a `ScanPaginator` that handles the pagination loop automatically.

Find the `ScanAllItems` stub in `repository.go` and implement it, following the `TODO(lab)` comment. Create a paginator with `dynamodb.NewScanPaginator(r.client, &dynamodb.ScanInput{TableName: ...})`, then loop while `paginator.HasMorePages()`, calling `paginator.NextPage(ctx)` and appending `page.Items` to your result slice. The paginator manages `LastEvaluatedKey` / `ExclusiveStartKey` across pages for you; each page contains up to 1 MB of data.

::::expand{header="Expand this to see the solution for ScanAllItems"}
```go
func (r *Repository) ScanAllItems(ctx context.Context) ([]map[string]types.AttributeValue, error) {
	var allItems []map[string]types.AttributeValue

	paginator := dynamodb.NewScanPaginator(r.client, &dynamodb.ScanInput{
		TableName: aws.String(r.tableName),
	})
	for paginator.HasMorePages() {
		page, err := paginator.NextPage(ctx)
		if err != nil {
			return nil, err
		}
		allItems = append(allItems, page.Items...)
	}
	return allItems, nil
}
```
::::

## Your turn: scan with a filter expression

Filter expressions reduce the items returned to the caller, but DynamoDB still reads and charges for all items scanned.

Find the `ScanOrdersByStatus` stub and implement it, following the `TODO(lab)` comment. It is the same paginator loop as `ScanAllItems`, but the `ScanInput` also carries:
- `FilterExpression`: `"#status = :status AND begins_with(sk, :order_prefix)"`
- `ExpressionAttributeNames`: `{"#status": "status"}` (`status` is a reserved word)
- `ExpressionAttributeValues`: `:status = string(status)`, `:order_prefix = "#ORDER#"`

::::expand{header="Expand this to see the solution for ScanOrdersByStatus"}
```go
func (r *Repository) ScanOrdersByStatus(ctx context.Context, status OrderStatus) ([]map[string]types.AttributeValue, error) {
	var allItems []map[string]types.AttributeValue

	paginator := dynamodb.NewScanPaginator(r.client, &dynamodb.ScanInput{
		TableName:        aws.String(r.tableName),
		FilterExpression: aws.String("#status = :status AND begins_with(sk, :order_prefix)"),
		ExpressionAttributeNames: map[string]string{
			"#status": "status",
		},
		ExpressionAttributeValues: map[string]types.AttributeValue{
			":status":       &types.AttributeValueMemberS{Value: string(status)},
			":order_prefix": &types.AttributeValueMemberS{Value: "#ORDER#"},
		},
	})

	for paginator.HasMorePages() {
		page, err := paginator.NextPage(ctx)
		if err != nil {
			return nil, err
		}
		allItems = append(allItems, page.Items...)
	}
	return allItems, nil
}
```
::::

::alert[Filter expressions do NOT reduce the amount of data read from disk or the capacity consumed. They only reduce the data sent back to the client. If you find yourself filtering heavily, consider creating an index instead.]{type="warning"}

This scan-and-filter for pending orders is exactly the access pattern the sparse `placed-index` GSI already serves. Earlier in this module you queried it with `GetPendingOrders`, which reads *only* the pending/confirmed orders directly from the index. Compare the two:

- **`ScanOrdersByStatus`** reads (and pays for) every item in the table, then discards the ones that don't match. Cost scales with the whole table.
- **`GetPendingOrders`** (sparse `placed-index`) reads only the items that carry a `placed_id`. Cost scales with just the active orders.

For a recurring, known query like "all pending orders," the sparse index is the right tool; a filtered scan is fine for one-off administrative or analytical reads where no suitable index exists.

## Your turn: parallel scan

For large tables, you can split the scan across multiple goroutines to increase throughput. Each segment reads a different portion of the table.

Find the `ParallelScan` stub and implement it, following the `TODO(lab)` comment. Launch `totalSegments` goroutines; each builds its own paginator with `Segment` set to its index and `TotalSegments` set to `totalSegments`, drains all its pages, and sends its items (or an error) back on a channel. The caller collects from the channel, returning the first error or the combined items.

DynamoDB divides the table's hash space evenly across segments. A good starting point is one segment per vCPU available to your application.

::::expand{header="Expand this to see the solution for ParallelScan"}
```go
func (r *Repository) ParallelScan(ctx context.Context, totalSegments int) ([]map[string]types.AttributeValue, error) {
	type segmentResult struct {
		items []map[string]types.AttributeValue
		err   error
	}

	results := make(chan segmentResult, totalSegments)

	for segment := 0; segment < totalSegments; segment++ {
		go func(seg int) {
			var items []map[string]types.AttributeValue

			paginator := dynamodb.NewScanPaginator(r.client, &dynamodb.ScanInput{
				TableName:     aws.String(r.tableName),
				Segment:       aws.Int32(int32(seg)),
				TotalSegments: aws.Int32(int32(totalSegments)),
			})

			for paginator.HasMorePages() {
				page, err := paginator.NextPage(ctx)
				if err != nil {
					results <- segmentResult{err: err}
					return
				}
				items = append(items, page.Items...)
			}

			results <- segmentResult{items: items}
		}(segment)
	}

	var allItems []map[string]types.AttributeValue
	for i := 0; i < totalSegments; i++ {
		result := <-results
		if result.err != nil {
			return nil, result.err
		}
		allItems = append(allItems, result.items...)
	}
	return allItems, nil
}
```
::::

::alert[Each stub's `// TODO(lab):` comment describes exactly what to do. If you get stuck, see the full reference solution as described in :link[Set up the Go project]{href="/dynamodb-for-go-developers/setup/step1"}.]{type="info"}

## Check your work

```bash
go run . demo
```

Expected fragment (item count depends on earlier steps):
```text
== Scan: full table count ==
  15 items in table
...
== Scan (filtered): all pending orders across the table ==
  3 pending order items matched the filter

== Scan (parallel): full table with 4 segments ==
  17 items read across 4 segments
```

The parallel-scan count is higher than the earlier full-table count because the demo's transaction and conditional-create steps add items before the scans run - the exact number depends on which earlier steps you have completed. Both the sequential and parallel scans return the same total, but parallel scan completes faster on large tables because segments are processed concurrently.

In the next module, you learn how to update items with expressions and conditions.
