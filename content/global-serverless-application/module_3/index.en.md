---
title : "Module 3: Interact with the Globalflix Interface"
weight : 40
---

### Navigate to the Globalflix Web App
  Click the link below to open the Globalflix web app, or if you still have the app open from module 2, click the Globalflix logo on the top right. 
  [https://amazon-dynamodb-labs.com/static/global-serverless-application/web/globalflix.html](https://amazon-dynamodb-labs.com/static/global-serverless-application/web/globalflix.html)

If you have already successfully loaded the API urls in the last module, you should see a grid of 12 video thumbnails. This has been displayed by performing a query against DynamoDB for the sample data you loaded in module 1.

The API region(s) you set in the previous module should be displayed on the top right, with the current "active" region in solid orange. 

1. Select the outlined region to perform a local "failover" to the second region

For the sake of time in this module we are executing this regional failover within the web application, but in production a more common pattern is to make use of something like [Amazon Route 53 Application Recovery Controller](https://aws.amazon.com/route53/application-recovery-controller/) to manage the health checks, failover, and recovery of your regional services.

![globalflix](/static/images/global-serverless-application/module_3/globalflix.png)


### Watch a video to start loading bookmarks into the database

2. Click on any of the videos to load the video player page. 

On this page, the selected video will start playing in the middle with the following metrics displayed around it (from left to right):

* Video Progress: Current Timestamp of your progress through the video as seen by your web browser
* Write Latency: Time in milliseconds it took to write the last bookmark to the database
* Region 1 and 2 Progress: Current Timestamp of your progress through the video when reading the bookmark item from each region

Underneath the player you can see a log of each write operation performed, note the region being used.

![player](/static/images/global-serverless-application/module_3/player.png)


### Simulate a Region Failure

3. Return to the AWS console and search for "Lambda" using the search bar at the top
4. A function named "global-serverless-dev" should be listed on the functions page, click the function name. If you do not see it listed check to make sure you are in one of the two regions you deployed to with Chalice on the top right of the page
5. Use the **Throttle** button on the top right of the page to set the Lambda functions maximum concurrency to 0, halting any future invocations of the function in this region.

![lambda_throttle](/static/images/global-serverless-application/module_3/lambda_throttle.png)

6. Switch back to the Globalflix video player and observe that an API failure in that region has been detected

![ui_error](/static/images/global-serverless-application/module_3/ui_error.png)

7. Wait for the application to wait to failover

![ui_failover](/static/images/global-serverless-application/module_3/ui_failover.png)

Even though the application stack in that region is now unresponsive, because we are using DynamoDB Global Tables, data updates are still being replicated into that region. When the service recovers, we need not worry about data loss during that outage.

You can verify this if you would like by running a query against the "global-serverless" DynamoDB Table in each of your regions

:::code{showCopyAction=true showLineNumbers=false language=bash}
aws dynamodb query \
    --table-name global-serverless \
    --region us-west-2 \
    --key-condition-expression "PK = :PK" \
    --expression-attribute-values '{":PK": {"S": "user10"}}' \
    --query 'Items[*].bookmark.S' \
    --output text | awk '{print $1": us-west-2"}'
aws dynamodb query \
    --table-name global-serverless \
    --region eu-west-1 \
    --key-condition-expression "PK = :PK" \
    --expression-attribute-values '{":PK": {"S": "user10"}}' \
    --query 'Items[*].bookmark.S' \
    --output text | awk '{print $1": eu-west-1"}'
:::

8. Return to the Lambda console and click "Edit concurrency" at the top right

![lambda_unthrottle](/static/images/global-serverless-application/module_3/lambda_unthrottle.png)

9. Select the "Use unreserved account concurrency" button and then Save

![lambda_concurrency](/static/images/global-serverless-application/module_3/lambda_concurrency.png)

Your resilient application has now successfully tolerated a failed regional stack, failed to an alternate region, and failed back, all with zero data loss or impact to the users experience.