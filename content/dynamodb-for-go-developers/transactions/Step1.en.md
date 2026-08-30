---
title: "TransactWriteItems"
date: 2021-04-21T07:33:04-05:00
weight: 10
---

[`TransactWriteItems`](https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_TransactWriteItems.html) ([Go SDK v2](https://pkg.go.dev/github.com/aws/aws-sdk-go-v2/service/dynamodb#Client.TransactWriteItems)) performs up to 100 write operations atomically. If any operation fails (due to a condition check, a conflict, or insufficient capacity), the entire transaction is rolled back. No partial writes occur. See [managing complex workflows with transactions](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/transaction-apis.html) for the full model.

## Use case: place an order atomically

When a user places an order, you need to:
1. Verify the user exists
2. Create the order
3. Create all order items

Without transactions, a failure partway through would leave orphaned items or an order without items. Transactions guarantee all-or-nothing.

## Worked example: place an order atomically

`PlaceOrder` is **provided for you** as this module's worked example - the `TransactWriteItems` pattern that the transactional read in the next step mirrors. Read it in `repository.go`. It builds a `[]types.TransactWriteItem` with three kinds of operations and passes them to `r.client.TransactWriteItems`:

1. **`ConditionCheck`** - verify the user's profile exists without modifying anything (`ConditionExpression: "attribute_exists(pk)"`). If the user doesn't exist, the entire transaction fails.
2. **`Put` (the order)** - the order item map keyed `pk = #USER#<UserID>`, `sk = #ORDER#<ID>`.
3. **`Put` (each item)** - one per element of `items`, keyed `pk = #ORDER#<ID>`, `sk = #ITEM#<ItemID>`.

```go
func (r *Repository) PlaceOrder(ctx context.Context, order *Order, items []OrderItem) error {
	var transactItems []types.TransactWriteItem

	transactItems = append(transactItems, types.TransactWriteItem{
		ConditionCheck: &types.ConditionCheck{
			TableName: aws.String(r.tableName),
			Key: map[string]types.AttributeValue{
				"pk": &types.AttributeValueMemberS{Value: fmt.Sprintf("#USER#%s", order.UserID)},
				"sk": &types.AttributeValueMemberS{Value: "PROFILE"},
			},
			ConditionExpression: aws.String("attribute_exists(pk)"),
		},
	})

	statusDate := fmt.Sprintf("%s#%s", order.Status, order.CreatedAt.Format("2006-01-02"))
	orderItem := map[string]types.AttributeValue{
		"pk":          &types.AttributeValueMemberS{Value: fmt.Sprintf("#USER#%s", order.UserID)},
		"sk":          &types.AttributeValueMemberS{Value: fmt.Sprintf("#ORDER#%s", order.ID)},
		"order_id":    &types.AttributeValueMemberS{Value: order.ID},
		"user_id":     &types.AttributeValueMemberS{Value: order.UserID},
		"status":      &types.AttributeValueMemberS{Value: string(order.Status)},
		"status_date": &types.AttributeValueMemberS{Value: statusDate},
		"placed_id":   &types.AttributeValueMemberS{Value: string(order.Status)},
		"address_key": &types.AttributeValueMemberS{Value: order.AddressKey},
		"created_at":  &types.AttributeValueMemberS{Value: order.CreatedAt.Format(time.RFC3339)},
		"updated_at":  &types.AttributeValueMemberS{Value: order.UpdatedAt.Format(time.RFC3339)},
	}
	transactItems = append(transactItems, types.TransactWriteItem{
		Put: &types.Put{TableName: aws.String(r.tableName), Item: orderItem},
	})

	for _, item := range items {
		transactItems = append(transactItems, types.TransactWriteItem{
			Put: &types.Put{
				TableName: aws.String(r.tableName),
				Item: map[string]types.AttributeValue{
					"pk":       &types.AttributeValueMemberS{Value: fmt.Sprintf("#ORDER#%s", order.ID)},
					"sk":       &types.AttributeValueMemberS{Value: fmt.Sprintf("#ITEM#%s", item.ItemID)},
					"order_id": &types.AttributeValueMemberS{Value: order.ID},
					"item_id":  &types.AttributeValueMemberS{Value: item.ItemID},
					"name":     &types.AttributeValueMemberS{Value: item.Name},
					"price":    &types.AttributeValueMemberN{Value: fmt.Sprintf("%.2f", item.Price)},
					"quantity": &types.AttributeValueMemberN{Value: fmt.Sprintf("%d", item.Quantity)},
				},
			},
		})
	}

	_, err := r.client.TransactWriteItems(ctx, &dynamodb.TransactWriteItemsInput{
		TransactItems: transactItems,
	})
	return err
}
```

All operations succeed or all fail - there is no state where you have an order without items or items without an order.

## Transaction limits

- Maximum **100 items** per transaction (including condition checks)
- Maximum **4 MB** total request size
- All items must be in the **same region**
- No two operations can target the **same item** within a transaction

## Idempotency

You can pass a `ClientRequestToken` to make a transaction idempotent:

```go
_, err := r.client.TransactWriteItems(ctx, &dynamodb.TransactWriteItemsInput{
	TransactItems:      transactItems,
	ClientRequestToken: aws.String("order-" + order.ID),
})
```

If the same token is sent within 10 minutes, DynamoDB returns success without re-executing the transaction. This protects against duplicate order placement due to retries.

## Check your work

The demo places a new order for alice using `PlaceOrder`:

```bash
go run . demo
```

Expected fragment:
```text
== Transaction: place a new order for alice ==
  Placed order ord-demo-txn with 1 item(s)
```

The transaction succeeds because alice exists. Had the condition check targeted a non-existent user, the entire transaction - including both `Put` operations - would have been rolled back with no items written.
