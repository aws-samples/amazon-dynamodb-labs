---
title: "PutItem - Create entities"
date: 2021-04-21T07:33:04-05:00
weight: 10
---

The [`PutItem`](https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_PutItem.html) operation ([Go SDK v2](https://pkg.go.dev/github.com/aws/aws-sdk-go-v2/service/dynamodb#Client.PutItem)) creates a new item or replaces an existing item with the same key. In this step, you implement the functions that create each entity type.

## The repository

All DynamoDB data-plane operations live in a `Repository` type in `repository.go`. The struct and its constructor are already provided:

```go
type Repository struct {
	client    *dynamodb.Client
	tableName string
}

func NewRepository(client *dynamodb.Client, tableName string) *Repository {
	return &Repository{
		client:    client,
		tableName: tableName,
	}
}
```

Notice there is no `CreateTable` function. The table was provisioned with CloudFormation in the previous module - application code only touches the data plane.

## Worked example: marshaling and creating a user

Two functions are already implemented for you as worked examples.

`marshalUser` converts a `User` struct into a DynamoDB attribute map, then sets the single-table keys by hand:

```go
func marshalUser(user User) (map[string]types.AttributeValue, error) {
	item, err := attributevalue.MarshalMap(user)
	if err != nil {
		return nil, err
	}
	item["pk"] = &types.AttributeValueMemberS{Value: fmt.Sprintf("#USER#%s", user.Username)}
	item["sk"] = &types.AttributeValueMemberS{Value: "PROFILE"}
	return item, nil
}
```

`attributevalue.MarshalMap` uses the `dynamodbav` struct tags to build the map. Because `User.Username` has the tag `dynamodbav:"-"`, it is excluded from marshaling. The username is encoded in the partition key instead of stored as a redundant attribute.

`CreateUser` marshals with that helper and writes the item with `PutItem`:

```go
func (r *Repository) CreateUser(ctx context.Context, user User) error {
	item, err := marshalUser(user)
	if err != nil {
		return err
	}
	_, err = r.client.PutItem(ctx, &dynamodb.PutItemInput{
		TableName: aws.String(r.tableName),
		Item:      item,
	})
	return err
}
```

## Your turn: marshal and create orders

Now implement the equivalent functions for orders. In `repository.go`, find the `marshalOrder` stub and complete it, following the `TODO(lab)` comment. Beyond `pk` and `sk`, an order carries two derived index attributes:

1. **`status_date`** - a composite attribute combining status and creation date (`<status>#<date>`). This is the sort key for the `status-date-index` LSI.
2. **`placed_id`** - set **only** when the order is `pending` or `confirmed`. This is what makes the `placed-index` GSI a sparse index - only active orders appear in it.

Then complete the `CreateOrder` stub, mirroring `CreateUser`.

Try to implement these yourself first. If you get stuck, expand the solution below and copy it into `repository.go`.

::::expand{header="Expand this to see the solution for marshalOrder and CreateOrder"}
```go
func marshalOrder(order Order) (map[string]types.AttributeValue, error) {
	item, err := attributevalue.MarshalMap(order)
	if err != nil {
		return nil, err
	}
	item["pk"] = &types.AttributeValueMemberS{Value: fmt.Sprintf("#USER#%s", order.UserID)}
	item["sk"] = &types.AttributeValueMemberS{Value: fmt.Sprintf("#ORDER#%s", order.ID)}
	item["status_date"] = &types.AttributeValueMemberS{Value: fmt.Sprintf("%s#%s", order.Status, order.CreatedAt.Format("2006-01-02"))}

	// placed_id is only present for active orders, which is what makes the placed-index sparse.
	if order.Status == OrderStatusPending || order.Status == OrderStatusConfirmed {
		item["placed_id"] = &types.AttributeValueMemberS{Value: string(order.Status)}
	}
	return item, nil
}

func (r *Repository) CreateOrder(ctx context.Context, order *Order) error {
	item, err := marshalOrder(*order)
	if err != nil {
		return err
	}
	_, err = r.client.PutItem(ctx, &dynamodb.PutItemInput{
		TableName: aws.String(r.tableName),
		Item:      item,
	})
	return err
}
```
::::

## Your turn: marshal and create order items

Complete the `marshalOrderItem` and `CreateOrderItem` stubs. Order items use the order ID as their partition key (`#ORDER#<orderID>`), so all items belonging to the same order are co-located and can be fetched in a single query.

::::expand{header="Expand this to see the solution for marshalOrderItem and CreateOrderItem"}
```go
func marshalOrderItem(orderID string, orderItem OrderItem) (map[string]types.AttributeValue, error) {
	item, err := attributevalue.MarshalMap(orderItem)
	if err != nil {
		return nil, err
	}
	item["pk"] = &types.AttributeValueMemberS{Value: fmt.Sprintf("#ORDER#%s", orderID)}
	item["sk"] = &types.AttributeValueMemberS{Value: fmt.Sprintf("#ITEM#%s", orderItem.ItemID)}
	return item, nil
}

func (r *Repository) CreateOrderItem(ctx context.Context, orderID string, orderItem *OrderItem) error {
	item, err := marshalOrderItem(orderID, *orderItem)
	if err != nil {
		return err
	}
	_, err = r.client.PutItem(ctx, &dynamodb.PutItemInput{
		TableName: aws.String(r.tableName),
		Item:      item,
	})
	return err
}
```
::::

::alert[Each stub's `// TODO(lab):` comment spells out the exact keys and attributes to set. If you get stuck, see the full reference solution as described in :link[Set up the Go project]{href="/dynamodb-for-go-developers/setup/step1"}.]{type="info"}

## Check your work

You have not implemented the bulk-load path yet, so run the demo to confirm your create functions compile. The demo seeds data first (via `SeedData`, which you implement in the next step) - for now, verify the project builds:

```bash
go build .
```

If it compiles cleanly, your `marshalOrder`, `marshalOrderItem`, `CreateOrder`, and `CreateOrderItem` implementations are syntactically sound. You test them against real data in the next step, once `BatchWriteItem` bulk-loads the sample dataset.
