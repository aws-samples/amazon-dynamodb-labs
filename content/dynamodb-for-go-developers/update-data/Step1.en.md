---
title: "UpdateItem with expressions"
date: 2021-04-21T07:33:04-05:00
weight: 10
---

The [`UpdateItem`](https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_UpdateItem.html) operation ([Go SDK v2](https://pkg.go.dev/github.com/aws/aws-sdk-go-v2/service/dynamodb#Client.UpdateItem)) modifies an existing item's attributes without replacing the entire item. This is more efficient than `PutItem` when you only need to change a few fields, because DynamoDB only writes the changed attributes.

## Update expressions

[Update expressions](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Expressions.UpdateExpressions.html) define what attributes to change. The four clauses are:

| Clause | Purpose | Example |
|--------|---------|---------|
| `SET` | Add or change attributes | `SET email = :email` |
| `REMOVE` | Delete attributes | `REMOVE placed_id` |
| `ADD` | Increment numbers or add to sets | `ADD quantity :inc` |
| `DELETE` | Remove elements from a set | `DELETE tags :old_tags` |

You can combine clauses in a single expression, but each keyword may appear **only once** - all your `SET` assignments go in one `SET` clause.

## Worked example: update order status

`UpdateOrderStatus` is **provided for you** as this module's worked example - the core `UpdateItem` pattern that the conditional update in the next step builds on. Read it in `repository.go`:

```go
func (r *Repository) UpdateOrderStatus(ctx context.Context, orderID string, newStatus OrderStatus) error {
	order, err := r.GetOrderByID(ctx, orderID)
	if err != nil {
		return err
	}

	statusDate := fmt.Sprintf("%s#%s", newStatus, time.Now().Format("2006-01-02"))

	// An UpdateExpression may use each keyword (SET/REMOVE) only once, so the
	// placed_id change is folded into the same SET or REMOVE clause rather than
	// appended as a second SET.
	setExpr := "SET #status = :status, #status_date = :status_date, #updated_at = :updated_at"
	exprNames := map[string]string{
		"#status":      "status",
		"#status_date": "status_date",
		"#updated_at":  "updated_at",
	}
	exprValues := map[string]types.AttributeValue{
		":status":      &types.AttributeValueMemberS{Value: string(newStatus)},
		":status_date": &types.AttributeValueMemberS{Value: statusDate},
		":updated_at":  &types.AttributeValueMemberS{Value: time.Now().Format(time.RFC3339)},
	}

	var updateExpr string
	if newStatus == OrderStatusPending || newStatus == OrderStatusConfirmed {
		// Active order: set placed_id so it appears in the sparse placed-index.
		setExpr += ", #placed_id = :placed_id"
		exprNames["#placed_id"] = "placed_id"
		exprValues[":placed_id"] = &types.AttributeValueMemberS{Value: string(newStatus)}
		updateExpr = setExpr
	} else {
		// Inactive order: drop placed_id so it falls out of the sparse index.
		exprNames["#placed_id"] = "placed_id"
		updateExpr = setExpr + " REMOVE #placed_id"
	}

	_, err = r.client.UpdateItem(ctx, &dynamodb.UpdateItemInput{
		TableName: aws.String(r.tableName),
		Key: map[string]types.AttributeValue{
			"pk": &types.AttributeValueMemberS{Value: fmt.Sprintf("#USER#%s", order.UserID)},
			"sk": &types.AttributeValueMemberS{Value: fmt.Sprintf("#ORDER#%s", orderID)},
		},
		UpdateExpression:          aws.String(updateExpr),
		ExpressionAttributeNames:  exprNames,
		ExpressionAttributeValues: exprValues,
	})
	return err
}
```

Three things to notice, which you reuse when you write the conditional update in the next step:

1. **Look up the order first** with `r.GetOrderByID(ctx, orderID)` to learn its `UserID` (needed for the base-table key).
2. **`status` is a reserved word**, so every attribute name is aliased via [`ExpressionAttributeNames`](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/ReservedWords.html) (the `#`-prefixed names).
3. **The sparse index is managed by the update:** `pending`/`confirmed` fold `#placed_id = :placed_id` into the same `SET` clause; any other status appends ` REMOVE #placed_id`, dropping the order from the sparse `placed-index`. Because `UpdateExpression` may use `SET` only once, the `placed_id` assignment must live in that same `SET` clause, not a second one.

## Check your work

Run the demo. The core walkthrough confirms an order (active status keeps `placed_id`) and then ships it (inactive status removes `placed_id`):

```bash
go run . demo
```

Expected fragment:
```text
== UpdateItem: confirm an order (active status -> keeps placed_id) ==
  ord-aaa-001  status=confirmed (now appears in confirmed placed-index)

== UpdateItem: ship an order (inactive status -> removes placed_id) ==
  ord-aaa-001  status=shipped (dropped from sparse placed-index)
```

By removing the `placed_id` attribute when an order becomes inactive, the order is automatically removed from the sparse GSI - no separate index maintenance required.
