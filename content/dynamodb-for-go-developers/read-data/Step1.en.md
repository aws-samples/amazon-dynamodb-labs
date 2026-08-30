---
title: "GetItem and Query"
date: 2021-04-21T07:33:04-05:00
weight: 10
---

The two primary read operations on the base table are `GetItem` (single item by key) and `Query` (multiple items sharing a partition key).

## GetItem - single item retrieval

The [`GetItem`](https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_GetItem.html) operation ([Go SDK v2](https://pkg.go.dev/github.com/aws/aws-sdk-go-v2/service/dynamodb#Client.GetItem)) retrieves a single item by its full primary key (partition key + sort key). It is the most efficient read operation in DynamoDB - it goes directly to the partition that holds the item.

`GetUser` is provided as a worked example. Read it in `repository.go`:

```go
func (r *Repository) GetUser(ctx context.Context, username string) (*User, error) {
	result, err := r.client.GetItem(ctx, &dynamodb.GetItemInput{
		TableName: aws.String(r.tableName),
		Key: map[string]types.AttributeValue{
			"pk": &types.AttributeValueMemberS{Value: fmt.Sprintf("#USER#%s", username)},
			"sk": &types.AttributeValueMemberS{Value: "PROFILE"},
		},
	})
	if err != nil {
		return nil, err
	}
	if result.Item == nil {
		return nil, fmt.Errorf("user not found: %s", username)
	}

	var user User
	if err := attributevalue.UnmarshalMap(result.Item, &user); err != nil {
		return nil, err
	}
	user.Username = username
	return &user, nil
}
```

`GetItem` requires the complete primary key. Because you know both the partition key (`#USER#alice`) and the sort key (`PROFILE`) for a user, you can fetch the exact item directly. `attributevalue.UnmarshalMap` converts the attribute map back into the Go struct using the `dynamodbav` tags.

### Consistent reads

By default, `GetItem` uses eventually consistent reads. If you need to read the most recent write immediately, request a strongly consistent read with `ConsistentRead: aws.Bool(true)` on the input. Strongly consistent reads cost twice as many Read Request Units (RRUs) - use them only when your application requires it.

### Projection expressions

If you only need certain attributes, set `ProjectionExpression: aws.String("full_name, email")` to reduce the payload transferred. The item still consumes the same RRUs (DynamoDB reads the full item internally), but you reduce network payload size.

## Query - retrieve collections

The [`Query`](https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_Query.html) operation ([Go SDK v2](https://pkg.go.dev/github.com/aws/aws-sdk-go-v2/service/dynamodb#Client.Query)) retrieves multiple items that share the same partition key, optionally filtering on the sort key with a [key condition expression](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Query.KeyConditionExpressions.html). This is how you retrieve hierarchically related data - for example, all orders belonging to a user.

`GetOrdersByUserID` is provided as a worked example:

```go
func (r *Repository) GetOrdersByUserID(ctx context.Context, userID string) ([]*Order, error) {
	result, err := r.client.Query(ctx, &dynamodb.QueryInput{
		TableName:              aws.String(r.tableName),
		KeyConditionExpression: aws.String("pk = :pk AND begins_with(sk, :sk_prefix)"),
		ExpressionAttributeValues: map[string]types.AttributeValue{
			":pk":        &types.AttributeValueMemberS{Value: fmt.Sprintf("#USER#%s", userID)},
			":sk_prefix": &types.AttributeValueMemberS{Value: "#ORDER#"},
		},
	})
	if err != nil {
		return nil, err
	}

	return unmarshalOrders(result.Items, userID), nil
}
```

The `KeyConditionExpression` has two parts:
- `pk = :pk` - matches the exact partition key for this user
- `begins_with(sk, :sk_prefix)` - matches only items whose sort key starts with `#ORDER#`

This excludes the user's `PROFILE` item and returns only the orders in that partition. The provided `unmarshalOrders` helper decodes each item, stamps the `userID`, and recovers each order's ID from its sort key.

## Your turn: get all items in an order

Find the `GetOrderItems` stub in `repository.go` and implement it, following the `TODO(lab)` comment. It is the same base-table `Query` shape as `GetOrdersByUserID`, but:
- `pk` = `#ORDER#<orderID>`
- the sort-key prefix is `#ITEM#`

Unmarshal each result into an `OrderItem` and return the slice.

::::expand{header="Expand this to see the solution for GetOrderItems"}
```go
func (r *Repository) GetOrderItems(ctx context.Context, orderID string) ([]OrderItem, error) {
	result, err := r.client.Query(ctx, &dynamodb.QueryInput{
		TableName:              aws.String(r.tableName),
		KeyConditionExpression: aws.String("pk = :pk AND begins_with(sk, :sk_prefix)"),
		ExpressionAttributeValues: map[string]types.AttributeValue{
			":pk":        &types.AttributeValueMemberS{Value: fmt.Sprintf("#ORDER#%s", orderID)},
			":sk_prefix": &types.AttributeValueMemberS{Value: "#ITEM#"},
		},
	})
	if err != nil {
		return nil, err
	}

	var items []OrderItem
	for _, item := range result.Items {
		var orderItem OrderItem
		if err := attributevalue.UnmarshalMap(item, &orderItem); err != nil {
			continue
		}
		items = append(items, orderItem)
	}
	return items, nil
}
```
::::

## Your turn: paginate a user's orders

When a query result exceeds 1 MB or you set a `Limit`, DynamoDB returns a `LastEvaluatedKey`. You pass it as `ExclusiveStartKey` in the next request to continue reading.

Find the `GetAllOrdersPaginated` stub and implement it, following the `TODO(lab)` comment. Run the same query as `GetOrdersByUserID` inside a loop: set `Limit` to `pageSize`, accumulate results each page, and continue while `LastEvaluatedKey` is non-nil, feeding it back in as `ExclusiveStartKey`.

For how DynamoDB paginates and the `LastEvaluatedKey` / `ExclusiveStartKey` contract, see the AWS documentation:

- [Paginating table query results](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Query.Pagination.html)
- [Working with queries in DynamoDB](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Query.html)
- [Go SDK v2: Client.Query](https://pkg.go.dev/github.com/aws/aws-sdk-go-v2/service/dynamodb#Client.Query)

::::expand{header="Expand this to see the solution for GetAllOrdersPaginated"}
```go
func (r *Repository) GetAllOrdersPaginated(ctx context.Context, userID string, pageSize int32) ([]*Order, error) {
	var allOrders []*Order
	var lastKey map[string]types.AttributeValue

	for {
		input := &dynamodb.QueryInput{
			TableName:              aws.String(r.tableName),
			KeyConditionExpression: aws.String("pk = :pk AND begins_with(sk, :sk_prefix)"),
			ExpressionAttributeValues: map[string]types.AttributeValue{
				":pk":        &types.AttributeValueMemberS{Value: fmt.Sprintf("#USER#%s", userID)},
				":sk_prefix": &types.AttributeValueMemberS{Value: "#ORDER#"},
			},
			Limit: aws.Int32(pageSize),
		}
		if lastKey != nil {
			input.ExclusiveStartKey = lastKey
		}

		result, err := r.client.Query(ctx, input)
		if err != nil {
			return nil, err
		}

		allOrders = append(allOrders, unmarshalOrders(result.Items, userID)...)

		lastKey = result.LastEvaluatedKey
		if lastKey == nil {
			break
		}
	}

	return allOrders, nil
}
```
::::

::alert[Each stub's `// TODO(lab):` comment describes exactly what to do. If you get stuck, see the full reference solution as described in :link[Set up the Go project]{href="/dynamodb-for-go-developers/setup/step1"}.]{type="info"}

## Check your work

Run the demo. If you have implemented the write path and these read functions, the demo progresses through the GetItem and base-table Query sections:

```bash
go run . demo
```

You should see alice's profile, her orders, and the items in one of them printed before the demo reaches the next unimplemented function. Sort order can be reversed with `ScanIndexForward: aws.Bool(false)` and results capped with `Limit` on any query.
