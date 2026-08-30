---
title: "Query Secondary Indexes"
date: 2021-04-21T07:33:04-05:00
weight: 20
---

Secondary indexes let you query data using different key patterns than the base table. In this step, you implement queries against both Global Secondary Indexes (GSIs) and the Local Secondary Index (LSI). All four functions in this step are `TODO(lab)` stubs - the key difference from a base-table query is the `IndexName` parameter, which tells DynamoDB to query an index instead of the base table.

Reference documentation for the exercises in this step:

- [Querying a Global Secondary Index](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GSI.html#GSI.Querying)
- [Querying a Local Secondary Index](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/LSI.html#LSI.Querying)
- [Improving data access with secondary indexes](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/SecondaryIndexes.html)
- [Multi-attribute keys for GSIs](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GSI.html)
- [Condition and key condition expressions](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Query.KeyConditionExpressions.html)
- [Go SDK v2: Client.Query](https://pkg.go.dev/github.com/aws/aws-sdk-go-v2/service/dynamodb#Client.Query)

## Inverted index GSI - find order by ID

The `inverted-index` GSI reverses the table's key schema: it uses `sk` as the partition key and `pk` as the sort key. This enables you to look up any item by its sort key value without knowing which partition it belongs to.

In a REST API, you often need to look up an order by its ID: `GET /orders/ord-aaa-001`. On the base table, orders are stored under the user's partition key (`pk = #USER#alice`), so you would need to know the user first. The inverted index solves this.

Find the `GetOrderByID` stub in `repository.go` and implement it, following the `TODO(lab)` comment:
- Set `IndexName` to `"inverted-index"`.
- Use `KeyConditionExpression` `"sk = :sk"` with `:sk = #ORDER#<orderID>` and `Limit: aws.Int32(1)`.
- The order's user is not stored as its own attribute - recover it from the returned item's `pk` by stripping the `#USER#` prefix, and set `order.ID = orderID` before returning.

::::expand{header="Expand this to see the solution for GetOrderByID"}
```go
func (r *Repository) GetOrderByID(ctx context.Context, orderID string) (*Order, error) {
	result, err := r.client.Query(ctx, &dynamodb.QueryInput{
		TableName:              aws.String(r.tableName),
		IndexName:              aws.String("inverted-index"),
		KeyConditionExpression: aws.String("sk = :sk"),
		ExpressionAttributeValues: map[string]types.AttributeValue{
			":sk": &types.AttributeValueMemberS{Value: fmt.Sprintf("#ORDER#%s", orderID)},
		},
		Limit: aws.Int32(1),
	})
	if err != nil {
		return nil, err
	}
	if len(result.Items) == 0 {
		return nil, fmt.Errorf("order not found: %s", orderID)
	}

	var order Order
	if err := attributevalue.UnmarshalMap(result.Items[0], &order); err != nil {
		return nil, err
	}
	if pkValue, ok := result.Items[0]["pk"]; ok {
		if pkStr, ok := pkValue.(*types.AttributeValueMemberS); ok {
			order.UserID = pkStr.Value[6:]
		}
	}
	order.ID = orderID
	return &order, nil
}
```
::::

::alert[GSI queries are always eventually consistent. You cannot use `ConsistentRead: true` with a GSI query.]{type="info"}

## Sparse index GSI - get pending orders

The `placed-index` GSI is a sparse index. Only items that have the `placed_id` attribute appear in this index. Orders have `placed_id` set only when their status is `pending` or `confirmed` (this is exactly the attribute your `marshalOrder` set conditionally). Once an order is shipped or delivered, the attribute is removed, and the order disappears from the index.

Sparse indexes are useful when you need to query a subset of items efficiently. Instead of scanning the entire table and filtering, you query an index that contains only the items you care about.

Find the `GetPendingOrders` stub and implement it, following the `TODO(lab)` comment:
- Set `IndexName` to `"placed-index"`.
- Use `KeyConditionExpression` `"placed_id = :placed_id"` with `:placed_id = string(OrderStatusPending)`.
- Unmarshal each returned item into an `*Order`.

::::expand{header="Expand this to see the solution for GetPendingOrders"}
```go
func (r *Repository) GetPendingOrders(ctx context.Context) ([]*Order, error) {
	result, err := r.client.Query(ctx, &dynamodb.QueryInput{
		TableName:              aws.String(r.tableName),
		IndexName:              aws.String("placed-index"),
		KeyConditionExpression: aws.String("placed_id = :placed_id"),
		ExpressionAttributeValues: map[string]types.AttributeValue{
			":placed_id": &types.AttributeValueMemberS{Value: string(OrderStatusPending)},
		},
	})
	if err != nil {
		return nil, err
	}

	var orders []*Order
	for _, item := range result.Items {
		var order Order
		if err := attributevalue.UnmarshalMap(item, &order); err != nil {
			continue
		}
		orders = append(orders, &order)
	}
	return orders, nil
}
```
::::

Because this is a sparse index, the query only reads items that are actually pending - not every order in the system.

### GSI write costs

Every time you write an item to the base table, DynamoDB also writes it to each GSI where the item's attributes match the GSI key schema. Adding `placed_id` to an order causes a write to the `placed-index` GSI; removing it causes a delete from the GSI. Sparse indexes are cost-efficient because they only contain the subset of items that have the index key attribute.

## Local Secondary Index - query by status and date

The `status-date-index` LSI shares the same partition key (`pk`) as the base table but uses `status_date` as the sort key. The `status_date` attribute is a composite string in the format `<status>#<date>`, for example `pending#2024-01-10` - the value your `marshalOrder` built.

| Feature | LSI | GSI |
|---------|-----|-----|
| Partition key | Same as base table | Can be different |
| Consistent reads | Yes (strongly consistent available) | No (always eventually consistent) |
| Created | Only at table creation time | Any time |
| Storage limit | 10 GB per partition key value | No limit |

Find the `GetUserOrdersByStatus` stub and implement it, following the `TODO(lab)` comment:
- Set `IndexName` to `"status-date-index"`.
- Use `KeyConditionExpression` `"pk = :pk AND begins_with(status_date, :status_prefix)"` with `:pk = #USER#<userID>` and `:status_prefix = string(status) + "#"`.
- Return `unmarshalOrders(result.Items, userID)`.

::::expand{header="Expand this to see the solution for GetUserOrdersByStatus"}
```go
func (r *Repository) GetUserOrdersByStatus(ctx context.Context, userID string, status OrderStatus) ([]*Order, error) {
	result, err := r.client.Query(ctx, &dynamodb.QueryInput{
		TableName:              aws.String(r.tableName),
		IndexName:              aws.String("status-date-index"),
		KeyConditionExpression: aws.String("pk = :pk AND begins_with(status_date, :status_prefix)"),
		ExpressionAttributeValues: map[string]types.AttributeValue{
			":pk":            &types.AttributeValueMemberS{Value: fmt.Sprintf("#USER#%s", userID)},
			":status_prefix": &types.AttributeValueMemberS{Value: string(status) + "#"},
		},
	})
	if err != nil {
		return nil, err
	}

	return unmarshalOrders(result.Items, userID), nil
}
```
::::

Because the `status_date` attribute has the format `pending#2024-01-10`, the `begins_with` condition returns all of the user's orders in that status, sorted chronologically. Unlike GSIs, LSIs support strongly consistent reads because the LSI data lives in the same partition as the base table data.

::alert[Each stub's `// TODO(lab):` comment describes exactly what to do. If you get stuck, see the full reference solution as described in :link[Set up the Go project]{href="/dynamodb-for-go-developers/setup/step1"}.]{type="info"}

## Check your work so far

Run the demo. With the inverted-index, sparse-index, and LSI queries implemented, the demo prints an order looked up by ID, all pending orders across users, and alice's pending orders:

```bash
go run . demo
```

Expected fragment:
```text
== Query: inverted-index GSI (find order by ID) ==
  ord-aaa-001  user=alice  status=pending

== Query: placed-index sparse GSI (all pending orders) ==
  ord-aaa-001  user=alice
  ord-bbb-001  user=bob
  ord-ccc-001  user=carol

== Query: status-date-index LSI (alice's pending orders) ==
  ord-aaa-001
```

## Multi-attribute keys - a modern alternative to the LSI

The LSI you just used relies on a manually concatenated `status_date` string (`pending#2024-01-10`). You had to build that string when writing the item, and query it with `begins_with`. This is the classic workaround for querying on more than one dimension.

As of November 2025, DynamoDB Global Secondary Indexes support **multi-attribute keys**: a GSI partition key can be composed of up to four attributes, and a sort key can be composed of up to four attributes. This lets you use your natural domain attributes directly instead of concatenating them into synthetic strings.

The `status-date-gsi` in the CloudFormation template uses this feature. Its sort key is composed of two independent attributes - `status` and `created_at` - rather than one concatenated string:

```yaml
- IndexName: status-date-gsi
  KeySchema:
    - AttributeName: pk
      KeyType: HASH
    - AttributeName: status      # first sort key attribute
      KeyType: RANGE
    - AttributeName: created_at  # second sort key attribute
      KeyType: RANGE
```

### Your turn: query the multi-attribute GSI

Find the `GetUserOrdersByStatusGSI` stub and implement it, following the `TODO(lab)` comment:
- Set `IndexName` to `"status-date-gsi"`.
- Use `KeyConditionExpression` `"pk = :pk AND #status = :status AND created_at > :since"`.
- `status` is a reserved word - alias it via `ExpressionAttributeNames` (`"#status" -> "status"`).
- Values: `:pk = #USER#<userID>`, `:status = string(status)`, `:since = since`.
- Return `unmarshalOrders(result.Items, userID)`.

Notice what changed compared to the LSI query:
- No concatenated string - `status` and `created_at` are queried as separate native attributes.
- The partition key uses an equality condition, each sort key attribute is applied left-to-right, and the range condition (`created_at > :since`) is on the last sort key attribute.
- Because `created_at` is a distinct attribute, you could store it as a Number type for numeric sorting instead of relying on lexicographic string order.

::::expand{header="Expand this to see the solution for GetUserOrdersByStatusGSI"}
```go
func (r *Repository) GetUserOrdersByStatusGSI(ctx context.Context, userID string, status OrderStatus, since string) ([]*Order, error) {
	result, err := r.client.Query(ctx, &dynamodb.QueryInput{
		TableName:              aws.String(r.tableName),
		IndexName:              aws.String("status-date-gsi"),
		KeyConditionExpression: aws.String("pk = :pk AND #status = :status AND created_at > :since"),
		ExpressionAttributeNames: map[string]string{
			"#status": "status",
		},
		ExpressionAttributeValues: map[string]types.AttributeValue{
			":pk":     &types.AttributeValueMemberS{Value: fmt.Sprintf("#USER#%s", userID)},
			":status": &types.AttributeValueMemberS{Value: string(status)},
			":since":  &types.AttributeValueMemberS{Value: since},
		},
	})
	if err != nil {
		return nil, err
	}

	return unmarshalOrders(result.Items, userID), nil
}
```
::::

### Query rules for multi-attribute sort keys

- All partition key attributes must use equality (`=`) conditions.
- Sort key attributes are queried **left-to-right** in the order defined - you can supply the first, the first two, and so on, but you cannot skip one in the middle.
- Range conditions (`>`, `<`, `BETWEEN`, `begins_with`) are only allowed on the **last** sort key attribute in your query.

### LSI vs. multi-attribute GSI

| | LSI (`status-date-index`) | Multi-attribute GSI (`status-date-gsi`) |
|--|--|--|
| Key composition | One concatenated `status_date` string | Separate `status` + `created_at` attributes |
| Application code | Must build/parse the composite string | Uses natural attributes directly |
| Consistent reads | Strongly consistent available | Eventually consistent only |
| Created | At table creation only | Any time |
| Native types | Everything is a string | Each attribute keeps its type |

Use the LSI when you need strongly consistent reads within a partition. Reach for multi-attribute GSIs when you want cleaner code, native typing, and the flexibility to add new query dimensions without reworking your item attributes.

### Check your work

```bash
go run . demo
```

Expected fragment:
```text
== Query: status-date-gsi multi-attribute GSI (alice's pending orders since 2024-01-01) ==
  ord-aaa-001  created=2024-01-10
```
