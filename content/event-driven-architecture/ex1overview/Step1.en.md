---
title: "AWS Event: Game Rules"
date: 2019-12-02T10:26:23-08:00
weight: 2
---

{{% notice info %}}
Points and scoreboard only apply when this lab is run during an AWS Event. If you're running this lab independently, you have the top score!
{{% /notice %}}
{{% notice info %}}
AWS Event: Be sure you've set a family-friendly team name in Workshop Studio, especially if you think you'll be on the top of the scoreboard!
{{% /notice %}}

To make this workshop more interesting we introduced a scoring element! As you move through the workshop and fix the pipeline you are awarded points for successfully aggregating messages.

Let's discuss how you earn points.

We'll begin by explaining how we generate messages and calculate the score. The upstream data source, the `GeneratorLambda` function, is invoked every 60 seconds by an EventBridge trigger. The `GeneratorLambda` function generates bursts of 10,000 messages that are ingested into the pipeline. This Lambda function also checks that all the messages were successfully aggregated at the end of the pipeline. If all messages have successfully arrived, with no losses or duplicates, within a time limit of 30 seconds then the participant receives 100 points.

Your task for *Lab 1* is to connect the different resources of the pipeline that were pre-created for you. If you do this successfully, you will start collecting points on the scoreboard starting with your first 100 points, and increasing to a maximum of 300 in *Lab 1*. You will be awarded 100 points every minute you have a working pipeline until you hit the maximum score for the first lab.

However, once you reach 300 points we're increasing the difficulty for you. In *Lab 2*, the `GeneratorLambda` intentionally writes duplicate records into the pipeline, and we introduce artificial random failures of your Lambda functions. Due to these challenges, your pipeline will initially not be able to accurately aggregate the ingested messages. Therefore, you will not receive additional points until you improve your pipeline to ensure accurate error handling and exactly once processing. This is the objective of *Lab 2*: if you have completed all parts, your pipeline can withstand duplicate messages and Lambda failures. Once you've successfully fixed the pipeline you will be awarded 100 points every 60 seconds for the duration of the workshop.

The workshop operators will display the scoring of all participants during the workshop, but you can check the scoreboard on your own.

Continue on to: [Connect the Pipeline]({{< ref "event-driven-architecture/ex2pipeline" >}})

or: [Optional - Pipeline Deep Dive]({{< ref "event-driven-architecture/ex1overview/step2.html" >}})
