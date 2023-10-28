---
title: "Step 2: Ensure idempotency of ReduceLambda function"
date: 2019-12-02T10:45:32-08:00
weight: 2
---


The objective of this step is to modify the `ReduceLambda` function to ensure idempotency, which means the values of the downstream `AggregateTable` will remain unchanged when old records are re-processed in the `ReduceLambda` function. DynamoDB transactions provide idempotency via the parameter `ClientRequestToken` that can be supplied with the  `TransactWriteItems` API operation. The `ClientRequestToken` makes sure that subsequent invocations of transactions with a token that was already used in the last 10 minutes don’t result in updates to the DynamoDB table.

We compute the hash over all messages in the batch that the Lambda function is invoked with to use as the `ClientRequestToken`. Lambda ensures that the function is retried with the same batch of messages on failure. Therefore, by ensuring that all code paths in the Lambda function are deterministic we can ensure idempotency of the transactions and achieve exactly once processing at this last stage of the pipeline. This method has a weakness because we only protect against re-processed messages within a 10-minute window after the first completed `TransactWriteItems` call since a `ClientRequestToken` is valid for no more than 10 minutes, as outlined [in the official documentation](https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_TransactWriteItems.html#DDB-TransactWriteItems-request-ClientRequestToken).


![Architecture-1](/images/event-driven-architecture/architecture/lab2-step2.png)

1. Navigate to the AWS Lambda service within the AWS Management console.
2. Click on the `ReduceLambda` function to edit its configuration.
3. Click on the `Code` tab to access the Lambda function's code.

Locate the following snippet in the Lambda function code:

```python
# Batch of Items
batch = [
    { 'Update':
        {
            'TableName' : constants.AGGREGATE_TABLE_NAME,
            'Key' : {constants.AGGREGATE_TABLE_KEY : {'S' : entry}},
            'UpdateExpression' : "ADD #val :val ",
            'ExpressionAttributeValues' : {
                ':val': {'N' : str(totals[entry])}
            },
            'ExpressionAttributeNames': {
                "#val" : "Value"
            }
        }
    } for entry in totals.keys()]

response = ddb_client.transact_write_items(
        TransactItems = batch
)
```

This section of code does the following:
- Creates a list of Python dictionaries containing entries corresponding to item operations to be processed by the `TransactWriteItems` API. To see all options for the field including `Update`, see the [API documentation](https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_TransactWriteItems.html).
- Specifically, each `Update` entry in the API call makes a modification to one DynamoDB item keyed by `entry` by atomically incrementing the `Value` attribute by the calculated total.

## Modify ddb_client.transact_write_items statement to include the ClientRequestToken

The code below contains two modifications:

* Computes a `ClientRequestToken` attribute as a hash value of all messages in the Lambda batch.
* Provides the `ClientRequestToken` as part of the DynamoDB `TransactWriteItems` API call.

```python
# Batch of Items
batch = [
    { 'Update':
        {
            'TableName' : constants.AGGREGATE_TABLE_NAME,
            'Key' : {constants.AGGREGATE_TABLE_KEY : {'S' : entry}},
            'UpdateExpression' : "ADD #val :val ",
            'ExpressionAttributeValues' : {
                ':val': {'N' : str(totals[entry])}
            },
            'ExpressionAttributeNames': {
                "#val" : "Value"
            }
        }
    } for entry in totals.keys()]

# Calculate hash to ensure this batch hasn't been processed already:
record_list_hash = hashlib.md5(str(records).encode()).hexdigest()

response = ddb_client.transact_write_items(
    TransactItems = batch,
    ClientRequestToken = record_list_hash
)
```

Apply these changes to your Lambda function code, either manually or just by copying the code snippet from above:

* Compute a hash over all the records in the batch (see line 18 in the previous snippet).
* Provide this hash to the `ddb_client.transact_write_items` function, as a `ClientRequestToken` (line 8 in the snippet above).
* Finally, click on `Deploy` to apply the changes.


## How do you know it is working?

Check your scoreboard. If all the previous steps are completed successfully you should start accumulating a score above 300 points. If not, check the CloudWatch Logs of the `ReduceLambda` function to check for any errors. If you see any errors, they may provide a hint on how to fix them. If you need help, go to `Summary & Conclusions` on the left, then `Solutions`, and you can see the desired code of the `ReduceLambda`.

{{% notice info %}}
Even if you've done everything correctly, the error rate won't drop to zero! The manually induced failures will still be there, but now the pipeline is able to sustain them and still ensure consistent aggregation.
{{% /notice %}}

Continue on  to: [Summary & Conclusions]({{< ref "event-driven-architecture/ex4summary" >}})

or: [Optional: Add a simple Python frontend]({{< ref "event-driven-architecture/ex3fixbugs/step3" >}})

