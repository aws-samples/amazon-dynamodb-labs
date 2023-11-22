---
title: "Ensure fault tolerance and exactly once processing"
date: 2019-12-02T10:17:22-08:00
weight: 4
chapter: true
pre: "<b>Lab 2: </b>"
description: "Query a sharded global secondary index to quickly read sorted data by status code and date."
---

::alert[Points and scoreboard only apply when this lab is run during an AWS Event.]

# Are you ready to start Lab 2?

Before proceeding to *Lab 2* let's verify that *Lab 1* was successfully completed. There are two phases to complete before continuing:
* First, you started to accumulate points on the scoreboard. If you have non-zero points then this phase is complete. Open the scoreboard and find your team. If you forgot to name your team in Workshop Studio, set your team name now and wait for the scoreboard to update.
* Second, you need accumulate 300 points to continue. The workshop will automatically switch to *Lab 2* when you reach this milestone, and this phase is complete.
 * Once 300 points are accumulated, new failure modes will be introduced and all three Lambda functions (`StateLambda`, `MapLambda`, and `ReduceLambda`) will start failing randomly. This is a pre-programmed evolution of the workshop. In the Lambda console, click on any of the three Lambda functions, navigate to  the `Monitor` tab and then to the `Metrics` sub-tab. You should expect to see a non-zero error rate on some of the graphs!

::alert[If the dashboard has 300 points, then congratulations: you can start Lab 2!]

![Architecture-1](/static/images/event-driven-architecture/lab2/failing-lambdas.png)


# Let’s utilize different features of DynamoDB to ensure data integrity and fault tolerance

In *Lab 2* we will achieve exactly once processing of the messages. To make sure that our pipeline can withstand different failure modes and achieve exactly once message processing.

![Architecture-3](/static/images/event-driven-architecture/architecture/after-lab-2.png)

Continue on to: :link[Step 1]{href="event-driven-architecture/ex3fixbugs/step1"}
