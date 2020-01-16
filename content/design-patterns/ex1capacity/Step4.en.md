+++
title = "Step 4 - View the CloudWatch metrics on your table"
date = 2019-12-02T10:26:29-08:00
weight = 6
+++


Open the browser tab to the AWS Management Console.

Then, open the DynamoDB section of the console by typing in *DynamoDB* in the search bar.

On the left pane click Tables, in the middle pane select table 'logfile', and on the right-most pane, click "Metrics".

**Figure - Open the CloudWatch metrics for the table**

![Open the CloudWatch metrics for the table](/images/awsconsole3.png)

**Figure - The CloudWatch metrics will look like the below for the base table**:

*Note: You may not see provisioned capacity data in your read or write capacity graphs, which are displayed as red lines. It takes time for DynamoDB to generate provisioned capacity CloudWatch metrics, especially on new tables.*
![The Cloud Watch metrics for the base table](/images/image1.jpg)

**Figure - The CloudWatch metrics will look like the below for the GSI**:
![The Cloud Watch metrics for the GSI](/images/image1-1.png)


**Topics for discussion:** *Why are there throttling events on the table but not on the GSI?*
