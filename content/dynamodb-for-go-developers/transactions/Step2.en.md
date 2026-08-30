---
title: "TransactGetItems"
date: 2021-04-21T07:33:04-05:00
weight: 20
---

[`TransactGetItems`](https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_TransactGetItems.html) ([Go SDK v2](https://pkg.go.dev/github.com/aws/aws-sdk-go-v2/service/dynamodb#Client.TransactGetItems)) reads up to 100 items atomically, returning a consistent snapshot across all items. This guarantees you see all items as they existed at the same point in time.

## Use case: fetch a complete order

When displaying an order to a user, you want to show the order details and all items in a consistent state. A regular `GetItem` + `Query` sequence could return results from different points in time if a write happens between the two calls.

## Your turn: implement GetOrderSnapshot

Find the `GetOrderSnapshot` stub in `repository.go` and implement it, following the `TODO(lab)` comment:

1. Call `r.GetOrderItems(ctx, orderID)` first, so you know which item keys to read.
2. Build a `[]types.TransactGetItem` whose **first** `Get` is the order (`pk = #USER#<userID>`, `sk = #ORDER#<orderID>`), followed by one `Get` per item (`pk = #ORDER#<orderID>`, `sk = #ITEM#<ItemID>`).
3. Call `r.client.TransactGetItems`. Responses come back in the **same order as the request**, so `result.Responses[0]` is the order and the rest are items.
4. Unmarshal the order (stamp `UserID` and `ID`) and each item, and return them.

::::expand{header="Expand this to see the solution for GetOrderSnapshot"}
```go
func (r *Repository) GetOrderSnapshot(ctx context.Context, userID, orderID string) (*Order, []OrderItem, error) {
	// The item IDs must be known up front to build the Get requests.
	orderItems, err := r.GetOrderItems(ctx, orderID)
	if err != nil {
		return nil, nil, err
	}

	var transactItems []types.TransactGetItem

	transactItems = append(transactItems, types.TransactGetItem{
		Get: &types.Get{
			TableName: aws.String(r.tableName),
			Key: map[string]types.AttributeValue{
				"pk": &types.AttributeValueMemberS{Value: fmt.Sprintf("#USER#%s", userID)},
				"sk": &types.AttributeValueMemberS{Value: fmt.Sprintf("#ORDER#%s", orderID)},
			},
		},
	})

	for _, item := range orderItems {
		transactItems = append(transactItems, types.TransactGetItem{
			Get: &types.Get{
				TableName: aws.String(r.tableName),
				Key: map[string]types.AttributeValue{
					"pk": &types.AttributeValueMemberS{Value: fmt.Sprintf("#ORDER#%s", orderID)},
					"sk": &types.AttributeValueMemberS{Value: fmt.Sprintf("#ITEM#%s", item.ItemID)},
				},
			},
		})
	}

	result, err := r.client.TransactGetItems(ctx, &dynamodb.TransactGetItemsInput{
		TransactItems: transactItems,
	})
	if err != nil {
		return nil, nil, err
	}

	var order Order
	if len(result.Responses) > 0 && result.Responses[0].Item != nil {
		if err := attributevalue.UnmarshalMap(result.Responses[0].Item, &order); err != nil {
			return nil, nil, err
		}
		order.UserID = userID
		order.ID = orderID
	}

	var items []OrderItem
	for _, resp := range result.Responses[1:] {
		if resp.Item != nil {
			var item OrderItem
			if err := attributevalue.UnmarshalMap(resp.Item, &item); err != nil {
				continue
			}
			items = append(items, item)
		}
	}

	return &order, items, nil
}
```
::::

## When to use TransactGetItems vs Query

For this specific example, a single `Query` on `pk = #ORDER#<id>` would be simpler and more efficient for retrieving items. `TransactGetItems` is most valuable when you need to read items from **different partitions** atomically:

- Reading a user profile AND an order from different partitions
- Reading multiple orders from different users simultaneously
- Any time you need a guaranteed point-in-time snapshot across partitions

::alert[The `// TODO(lab):` comment describes exactly what to do. If you get stuck, see the full reference solution as described in :link[Set up the Go project]{href="/dynamodb-for-go-developers/setup/step1"}.]{type="info"}

## Check your work

The demo reads an order and its items back as a consistent snapshot:

```bash
go run . demo
```

Expected fragment:
```text
== TransactGetItems: consistent snapshot of an order + its items ==
  order ord-bbb-001 (status=pending) with 2 item(s)
```

All data was read at a consistent point in time.

## You've completed every operation

If the demo now runs to `Demo complete.` without a `TODO(lab)` error, you have implemented every DynamoDB operation the workshop teaches. In the next module, you clean up the resources you created.
