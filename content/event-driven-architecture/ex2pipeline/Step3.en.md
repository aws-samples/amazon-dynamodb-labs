---
title: "Step 3: Connect ReduceLambda"
date: 2019-12-02T10:35:42-08:00
weight: 3
---

The objective of this last step in *Lab 1* is to correctly configure the `ReduceLambda` function, connect it to the DynamoDB stream of `ReduceTable`, and ensure the total aggregates are written to the `AggregateTable`. When you successfully complete this step, you will begin to accumulate points on the scoreboard.

![Architecture-1](/static/images/event-driven-architecture/architecture/step3.png)

## Configure Lambda concurrency

We start by setting the concurrency of the `ReduceLambda` function to `1`. This ensures that there is only a single active instance of the `ReduceLambda` function at any time. This is desired because we want to avoid write conflicts, where multiple instances attempt to update the `AggregateTable` at the same time.
From a performance point-of-view, a single Lambda instance can handle the aggregation of the entire pipeline because incoming messages are already pre-aggregated by the `MapLambda` functions.
<!-- TODO clarify what we mean by write conflicts -->
1. Navigate to the AWS Lambda service within the AWS Management Console.
2. Click on the function `ReduceLambda` to edit its configuration (see figure below).
3. Open the `Configuration` tab, then select `Concurrency` on the left.
4. Click the `Edit` button in the top right corner, select `Reserve concurrency` and enter `1`.
5. After you clicked `Save`, your configuration should look like the image below.

![Architecture-1](/static/images/event-driven-architecture/lab1/reduce-lambda-concurrency.png)

## Connect the ReduceLambda to the ReduceTable stream

Next, we want to connect the `ReduceLambda` function to the DynamoDB stream of the `ReduceTable`.

1. The function overview shows that the `ReduceLambda` function does not have a trigger. Click on the button `Add trigger`.
![Architecture-1](/static/images/event-driven-architecture/lab1/add-trigger-reduce-lambda.png)

2. Specify the following configuration:
    - In the drop down select `DynamoDB` as the data source.
    - In the DynamoDB table select `ReduceTable`.
    - Set `Batch size` to `1000`.

3. Click the `Add` button in the bottom right corner.

::alert[You will see an error here! Before we can enable this trigger we need to add IAM permissions to this Lambda functions.]{type="warning"}

![Architecture-1](/static/images/event-driven-architecture/lab1/reduce-lambda-error-permissions.png)

## Add required IAM permissions

The error message above informs you that the `ReduceLambda` function doesn't have the necessary permissions to read from the stream of the `ReduceTable`. While we have already assigned IAM roles with the required privileges to the `StateLambda` and the `MapLambda`, it's left to you to do it for the `ReduceLambda` function:

1. Keep your current Lambda console tab open on the page where you received the IAM error trying to add the trigger to the `ReduceLambda` function. Shortly you will need it open to retry the request.
2. Open a new browser tab, go the AWS Lambda service and select the `ReduceLambda` function.
3. Navigate to the `Configuration` tab and click on `Permissions`. You should see the Lambda execution role called `ReduceLambdaRole`. Click on this role to modify it.

![Architecture-1](/static/images/event-driven-architecture/lab1-permissions/click_on_role.png)

4. Now you're redirected to the IAM service, where you see the details of the `ReduceLambdaRole`. There is a policy associated with this role, the `ReduceLambdaPolicy`. Expand the view to see the current permissions of the `ReduceLambda` function. Now, click on the button `Edit` to add additional permissions.

![Architecture-1](/static/images/event-driven-architecture/lab1-permissions/click_on_edit_policy.png)

### Modify the IAM policy  
::alert[There is already an IAM permission in place for DynamoDB: this is necessary to ensure the workshop runs as expected. Don't get confused by this and please don't delete the permissions we've already granted! All of the Lambda functions need to be able to access the ParameterTable to check the current progress of the lab and the respective failure modes.]

* First we need to add permissions so the `ReduceLambda` function is able to read messages from the stream of the `ReduceTable`.
    * Click on `Add new statement`
      ![Architecture-1](/static/images/event-driven-architecture/lab1-permissions/click_add_new_statement.png)
    * For `Service`, select `DynamoDB`
    * Under `Access level - read`, check the following four checkboxes: `DescribeStream`, `GetRecords`, `GetShardIterator`, and `ListStreams`


Now we need to associate these permissions with specific resources (e.g. we want the `ReduceLambda` to be able to read exclusively from the `ReduceTable` alone). Hence, under `Add a resouce`, and click on `Add`. Then in `Resource type` choose `stream`. Next, fill out the following:
 * `{Region}` - The lab defaults to us-west-2, but verify your region and ensure the correct one is entered
 * `{Account}` - The AWS account id. You can put an asterisk here if you don't want to get the exact account id.
 * `{TableName}` - The name should be `ReduceTable`
 * `{StreamLabel}` - Add an asterisk `*` so that any stream label is supported. A Stream label is a unique identifier for a DynamoDB stream.
* Finally, click on `Add resource`. You've now granted permission for the `ReduceLambda` to read from the `ReduceTable` stream, but there is more to be done still.

::alert[Be sure to remove all curly braces from your ARN before clicking `Add resource`]

![Architecture-1](/static/images/event-driven-architecture/lab1-permissions/resource_stream.png)

If we make no further change, the `ReduceLambda` function will not be able to update the final results in the `AggregateTable`. We must modify the policy to add additional permissions to grant `UpdateItem` access to the function.
 * Click on `Add new statement`
 * For `Service`, select  `DynamoDB`
 * Under `Access level - read or write`, select the checkbox `UpdateItem`
* Again, we want to associate theses permissions with a specific resources: We want the `ReduceLambda` to be able to write to the `AggregateTable` alone. Hence, click on `Add a resource` and in the `Resource type` drop down choose `table`. Next, enter the values for `Region` (using the same region as before), `Account` (consider using an asterisk `*`), and `TableName` (this time it should be `AggregateTable`).
* Click `Add resource`.

![Architecture-1](/static/images/event-driven-architecture/lab1-permissions/resource_stream_2.png)

* Finally, click `Next` and then `Save changes` in the bottom right corner.

## Try again to connect ReduceLambda to the ReduceTable stream

If all of the above steps are executed correctly you will be able to connect the `ReduceLambda` to the DynamoDB stream of the `ReduceTable` by switching back to the open tab and again trying to click on `Add`. You may need to wait a couple of seconds for the IAM policy changes to propagate.

::alert[If you're not able to add the trigger, this may be due to a misconfiguration of the IAM policy. If you need help, go to `Summary & Conclusions` on the left, then `Solutions`, and you should see the desired `ReduceLambdaPolicy`.]

## How do you know it is working?

If everything was done right, then the DynamoDB stream of the `ReduceTable` should trigger the `ReduceLambda`. Therefore, you should be able to see logs for each Lambda invocation under the `Monitor` -> `Logs` tab.

Another way to verify it is working is to observe the items written by `ReduceLambda` to the DynamoDB table `AggregateTable`. To do that, navigate to the DynamoDB service in the AWS console, click `Items` on the left, and select `AggregateTable`. At this stage you should see multiple rows similar to the image below.

![AggregateTable items](/static/images/event-driven-architecture/lab1/aggregate-table-items.png)

::alert[AWS Event: If Steps 1, 2, and 3 of *Lab 1* were completed successfully you should start gaining score points within one to two minutes. Please check the scoreboard! Ask your lab moderator to provide a link to the scoreboard.]

Continue on to: :link[Lab 2]{href="/event-driven-architecture/ex3fixbugs"}
