---
title: "Step 2: Check MapLambda trigger"
date: 2019-12-02T10:35:42-08:00
weight: 2
---

{{% notice info %}}
The `MapLambda` function is already connected for you, so let us quickly check if it works as expected!
{{% /notice %}}

![Architecture-1](/static/images/event-driven-architecture/architecture/step2.png)

Check that `MapLambda` has a correctly configured trigger to receive messages from the `StateTable` stream:

1. Navigate to the AWS Lambda service within the AWS Management Console.
2. Click on the `MapLambda` function to view its configuration.
3. Verify that the `MapLambda` function has a DynamoDB trigger and this trigger points to the `StateTable` (see figure below).

![Architecture-1](/static/images/event-driven-architecture/target/TargetMapLambda.png)

## How do you know it is working?

Any row written to the `StateTable` should trigger the `MapLambda` function. Therefore, you should be able to see logs for the Lambda invocations.

Alternatively, you can observe the outputs of the `MapLambda` function in the DynamoDB `ReduceTable`. To do that, navigate to the DynamoDB service in the AWS console, click `Items` on the left, and select `ReduceTable`. At this stage you should see multiple rows similar to the image below.

![Reduce table items](/static/images/event-driven-architecture/lab1/reduce-table-items.png)

Continue on to: [Step 3]({{< ref "event-driven-architecture/ex2pipeline/step3" >}}).
