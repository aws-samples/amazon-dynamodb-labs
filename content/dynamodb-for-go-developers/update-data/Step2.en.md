---
title: "Condition expressions"
date: 2021-04-21T07:33:04-05:00
weight: 20
---

[Condition expressions](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Expressions.ConditionExpressions.html) let you specify requirements that must be true for a write to succeed. If the condition evaluates to false, DynamoDB rejects the write and returns a `ConditionalCheckFailedException`. This provides optimistic locking without external coordination. Conditions attach to the write operations you already know - [`UpdateItem`](https://pkg.go.dev/github.com/aws/aws-sdk-go-v2/service/dynamodb#Client.UpdateItem) and [`PutItem`](https://pkg.go.dev/github.com/aws/aws-sdk-go-v2/service/dynamodb#Client.PutItem).

## Why conditions matter

Without conditions, any write blindly overwrites the current state. Conditions prevent:
- Shipping an order that has already been cancelled
- Creating a user that already exists
- Updating a record that another process has already modified

## Your turn: conditional update - only ship confirmed orders

Find the `ShipOrder` stub in `repository.go` and implement it, following the `TODO(lab)` comment. The function should:

1. Look up the order with `r.GetOrderByID(ctx, orderID)` for its `UserID`.
2. `UpdateItem` with:
   - `UpdateExpression`: `"SET #status = :new_status, #status_date = :status_date REMOVE #placed_id"`
   - `ConditionExpression`: `"#status = :expected_status"` with `:expected_status = "confirmed"`
3. Alias `status`, `status_date`, and `placed_id` via `ExpressionAttributeNames`.

The `ConditionExpression` ensures the order's current status is `confirmed`. If someone already cancelled or shipped the order, the condition fails and the update is rejected.

::::expand{header="Expand this to see the solution for ShipOrder"}
```go
func (r *Repository) ShipOrder(ctx context.Context, orderID string) error {
	order, err := r.GetOrderByID(ctx, orderID)
	if err != nil {
		return err
	}

	statusDate := fmt.Sprintf("shipped#%s", time.Now().Format("2006-01-02"))

	_, err = r.client.UpdateItem(ctx, &dynamodb.UpdateItemInput{
		TableName: aws.String(r.tableName),
		Key: map[string]types.AttributeValue{
			"pk": &types.AttributeValueMemberS{Value: fmt.Sprintf("#USER#%s", order.UserID)},
			"sk": &types.AttributeValueMemberS{Value: fmt.Sprintf("#ORDER#%s", orderID)},
		},
		UpdateExpression:    aws.String("SET #status = :new_status, #status_date = :status_date REMOVE #placed_id"),
		ConditionExpression: aws.String("#status = :expected_status"),
		ExpressionAttributeNames: map[string]string{
			"#status":      "status",
			"#status_date": "status_date",
			"#placed_id":   "placed_id",
		},
		ExpressionAttributeValues: map[string]types.AttributeValue{
			":new_status":      &types.AttributeValueMemberS{Value: "shipped"},
			":expected_status": &types.AttributeValueMemberS{Value: "confirmed"},
			":status_date":     &types.AttributeValueMemberS{Value: statusDate},
		},
	})
	return err
}
```
::::

## Your turn: conditional create - prevent duplicate users

Conditions work with `PutItem` too. Find the `CreateUserIfNotExists` stub and implement it, following the `TODO(lab)` comment. It is like the `CreateUser` worked example, but adds `ConditionExpression: aws.String("attribute_not_exists(pk)")` to the `PutItemInput`. If a user with that username already has a profile, the write fails instead of silently overwriting it.

::::expand{header="Expand this to see the solution for CreateUserIfNotExists"}
```go
func (r *Repository) CreateUserIfNotExists(ctx context.Context, user User) error {
	item, err := marshalUser(user)
	if err != nil {
		return err
	}
	_, err = r.client.PutItem(ctx, &dynamodb.PutItemInput{
		TableName:           aws.String(r.tableName),
		Item:                item,
		ConditionExpression: aws.String("attribute_not_exists(pk)"),
	})
	return err
}
```
::::

## Handling ConditionalCheckFailedException

In Go, you detect a failed condition with the SDK's typed error and `errors.As`:

```go
import "errors"

var condErr *types.ConditionalCheckFailedException

if errors.As(err, &condErr) {
	fmt.Println("Condition not met — the item was not in the expected state.")
} else if err != nil {
	log.Fatalf("Unexpected error: %v", err)
}
```

The demo harness already uses this pattern when calling `ShipOrder` and `CreateUserIfNotExists`, so you can see both the success and rejection paths.

::alert[Each stub's `// TODO(lab):` comment describes exactly what to do. If you get stuck, see the full reference solution as described in :link[Set up the Go project]{href="/dynamodb-for-go-developers/setup/step1"}.]{type="info"}

## Check your work

```bash
go run . demo
```

Expected fragment:
```text
== PutItem (conditional): create a user only if absent ==
  created user 'dave'
...
== UpdateItem (conditional): ship a confirmed order ==
  ord-aaa-002 shipped (was confirmed)

== UpdateItem (conditional): try to ship a pending order (expect rejection) ==
  REJECTED as expected: order is not 'confirmed'
```

The condition expression enforced the business rule: orders must be confirmed before they can be shipped. The attempt to ship a pending order was rejected because its status was not `confirmed`.
