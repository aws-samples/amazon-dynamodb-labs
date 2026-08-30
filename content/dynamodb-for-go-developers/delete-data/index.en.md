---
title: "6. Delete Data"
date: 2021-04-21T07:33:04-05:00
weight: 60
description: "Delete items with conditions and handle related data cleanup."
---

The [`DeleteItem`](https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_DeleteItem.html) operation ([Go SDK v2](https://pkg.go.dev/github.com/aws/aws-sdk-go-v2/service/dynamodb#Client.DeleteItem)) removes a single item from the table by its primary key. DynamoDB does not have foreign keys or cascade deletes, so cleaning up related items is your responsibility.

## Worked example: delete a single item

`DeleteOrderItem` is **provided for you** as this module's worked example - a direct delete by full primary key. Read it in `repository.go`:

```go
func (r *Repository) DeleteOrderItem(ctx context.Context, orderID, itemID string) error {
	_, err := r.client.DeleteItem(ctx, &dynamodb.DeleteItemInput{
		TableName: aws.String(r.tableName),
		Key: map[string]types.AttributeValue{
			"pk": &types.AttributeValueMemberS{Value: fmt.Sprintf("#ORDER#%s", orderID)},
			"sk": &types.AttributeValueMemberS{Value: fmt.Sprintf("#ITEM#%s", itemID)},
		},
	})
	return err
}
```

`DeleteItem` is idempotent - deleting an item that doesn't exist does not produce an error. The two functions you write next build on this shape: one adds a condition, the other cascades across related items.

## Your turn: conditional delete

You can protect deletes with conditions. Find the `CancelOrder` stub and implement it, following the `TODO(lab)` comment: look up the order for its `UserID`, then `DeleteItem` the order (`pk = #USER#<UserID>`, `sk = #ORDER#<orderID>`) with:
- `ConditionExpression`: `"#status = :expected"` with `:expected = string(OrderStatusPending)`
- `ExpressionAttributeNames`: `{"#status": "status"}`
- `ReturnValues`: `types.ReturnValueAllOld`

This only allows cancelling an order that is still pending. `ReturnValues: AllOld` returns the attributes of the item as it was before deletion - useful for logging or confirmation.

::::expand{header="Expand this to see the solution for CancelOrder"}
```go
func (r *Repository) CancelOrder(ctx context.Context, orderID string) error {
	order, err := r.GetOrderByID(ctx, orderID)
	if err != nil {
		return err
	}

	_, err = r.client.DeleteItem(ctx, &dynamodb.DeleteItemInput{
		TableName: aws.String(r.tableName),
		Key: map[string]types.AttributeValue{
			"pk": &types.AttributeValueMemberS{Value: fmt.Sprintf("#USER#%s", order.UserID)},
			"sk": &types.AttributeValueMemberS{Value: fmt.Sprintf("#ORDER#%s", orderID)},
		},
		ConditionExpression: aws.String("#status = :expected"),
		ExpressionAttributeNames: map[string]string{
			"#status": "status",
		},
		ExpressionAttributeValues: map[string]types.AttributeValue{
			":expected": &types.AttributeValueMemberS{Value: string(OrderStatusPending)},
		},
		ReturnValues: types.ReturnValueAllOld,
	})
	return err
}
```
::::

## Your turn: delete an order and its items (cascade)

Because DynamoDB has no cascade delete, you must explicitly query for related items and delete them. Find the `DeleteOrderWithItems` stub and implement it, following the `TODO(lab)` comment:

1. `r.GetOrderItems(ctx, orderID)` and call `r.DeleteOrderItem` for each item.
2. `r.GetOrderByID(ctx, orderID)` to learn the `UserID`, then `DeleteItem` the order itself.

This approach has a weakness: it is **not atomic**. If the process crashes between deleting items and deleting the order, you are left in an inconsistent state. In the next module, you learn how transactions solve this problem.

::::expand{header="Expand this to see the solution for DeleteOrderWithItems"}
```go
func (r *Repository) DeleteOrderWithItems(ctx context.Context, orderID string) error {
	items, err := r.GetOrderItems(ctx, orderID)
	if err != nil {
		return err
	}

	for _, item := range items {
		if err := r.DeleteOrderItem(ctx, orderID, item.ItemID); err != nil {
			return fmt.Errorf("failed to delete item %s: %w", item.ItemID, err)
		}
	}

	order, err := r.GetOrderByID(ctx, orderID)
	if err != nil {
		return err
	}

	_, err = r.client.DeleteItem(ctx, &dynamodb.DeleteItemInput{
		TableName: aws.String(r.tableName),
		Key: map[string]types.AttributeValue{
			"pk": &types.AttributeValueMemberS{Value: fmt.Sprintf("#USER#%s", order.UserID)},
			"sk": &types.AttributeValueMemberS{Value: fmt.Sprintf("#ORDER#%s", orderID)},
		},
	})
	return err
}
```
::::

::alert[Each stub's `// TODO(lab):` comment describes exactly what to do. If you get stuck, see the full reference solution as described in :link[Set up the Go project]{href="/dynamodb-for-go-developers/setup/step1"}.]{type="info"}

## Check your work

```bash
go run . demo
```

Expected fragment:
```text
== DeleteItem: remove an order item ==
  order ord-aaa-001 now has 1 item(s)
...
== DeleteItem (cascade): delete an order and all its items ==
  deleted ord-ccc-001 and its items

== DeleteItem (conditional): cancel a pending order ==
  cancelled ord-bbb-001 (was pending)
```

In the next module, you learn how to use transactions to perform multiple operations atomically.
