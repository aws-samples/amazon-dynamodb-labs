---
title : "Module 1: Deploy the backend resources"
weight : 20
---

### Login to AWS Workshop Studio Portal

On the event dashboard, click on **Open AWS console** to federate into AWS Management Console in a new tab. On the same page, click **Get started** to open the workshop instructions.
![Event dashboard](/static/images/common/workshop-studio-01.png)

In addition to the AWS console you should open your Visual Studio code server, by clicking in the `VSCodeServerURL` parameter, available from the "Event Outputs" section. When prompted for a password use the value from `VSCodeServerPassword`. 

![Event dashboard](/static/images/common/workshop-studio-02.png)

During the first 60 seconds, the environment will automatically update extensions and plugins. Any startup notification can be safely dismissed. 
 
![VS Code Setup](/static/images/common/common-vs-code-01.png)

If a terminal is not available at the bottom left side of your screen, please open a new one like the following picture indicates.

![VS Code Setup](/static/images/common/common-vs-code-02.png)

Then run the command `aws sts get-caller-identity` just to verify that your AWS credentials have been properly configured.

![VS Code Setup](/static/images/common/common-vs-code-03.png)


From within the terminal:

To keep our python files and dependencies organized lets create a python virtual environment, in the LMR folder:

```bash
cd LMR
python -m venv .venv
source .venv/bin/activate
```

Your VS Code environment is already configured with boto3, but for this lab we will also need [AWS Chalice](https://github.com/aws/chalice). 

```bash
pip install chalice 
```

::alert[You may see a couple of WARNING lines near the bottom of the command output, these are safely ignored.]{type="info"}

Download the global serverless workshop:

```bash 
curl -O https://amazon-dynamodb-labs.com/assets/global-serverless.zip
unzip global-serverless.zip && cd global-serverless
```

To see what application resources we will be deploying you can open the **app.py** file by navigating to "global-serverless/app.py" in the file explorer. This code defines Lambda function and API Gateway routes.

### Deploy a new DynamoDB table
1. In your terminal, run:

:::code{showCopyAction=true showLineNumbers=false language=bash}
aws dynamodb create-table \
  --region us-west-2 \
  --table-name global-serverless \
  --attribute-definitions \
    AttributeName=PK,AttributeType=S \
    AttributeName=SK,AttributeType=S \
  --key-schema \
    AttributeName=PK,KeyType=HASH \
    AttributeName=SK,KeyType=RANGE \
  --billing-mode PAY_PER_REQUEST \
  --query '{"New Table ":TableDescription.TableArn, 
            "Status    ":TableDescription.TableStatus }'
:::

2. Wait a moment for the table to be created. 

Check to see when the table status changes from `CREATING` to `ACTIVE` by 
running this command:

:::code{showCopyAction=true showLineNumbers=false language=bash}
aws dynamodb describe-table \
  --table-name global-serverless \
  --region us-west-2 \
  --query '{TableStatus: Table.TableStatus}'
:::

3.Our table is in us-west-2 (Oregon). 
Let's make it a **Global Table** by requesting a replica in eu-west-1 (Europe/Dublin).

Run this command to create a new replica in the eu-west-1 (Europe/Dublin) 
region:

:::code{showCopyAction=true showLineNumbers=false language=bash}
aws dynamodb update-table --table-name global-serverless --region us-west-2 --cli-input-json  \
'{"ReplicaUpdates": [
    {
        "Create": {"RegionName": "eu-west-1" }
        }
    ]}'
:::

Check to see when the table replica status changes to `ACTIVE` by 
running this command:

:::code{showCopyAction=true showLineNumbers=false language=bash}
aws dynamodb describe-table \
  --table-name global-serverless \
  --region us-west-2 \
  --query '{TableStatus: Table.TableStatus,
               Replicas: Table.Replicas}'
:::

4. Next, add some data to the table:
Writing to a Global Table is done by writing to any of the regional replica tables.

Run this command to load video library items into the table with 
batch-write-item:

:::code{showCopyAction=true showLineNumbers=false language=bash}
aws dynamodb batch-write-item \
  --region us-west-2 \
  --request-items file://sample-data.json
:::

These items are how the UI will display which videos are available to stream.


5. Verify data was written:

:::code{showCopyAction=true showLineNumbers=false language=bash}
aws dynamodb get-item \
  --table-name global-serverless \
  --region us-west-2 \
  --key '{"PK": {"S": "library"}, "SK": {"S": "01"}}'
:::

### Deploy the backend API service to the first region

1. Run the following instruction to instruct Chalice to deploy into us-west-2 for our first region
```bash 
export AWS_DEFAULT_REGION=us-west-2
``` 

2. Run the following instruction and wait for the infrastructure to be created. Chalice is a Python based serverless framework.
```bash
chalice deploy
```

3. When the script completes, it reports a list of resources deployed. **Copy and paste the Rest API URL into a note as you will need it later.**
4. Copy that REST API URL and paste it into a new browser tab to test it. You should see a JSON response of `{ping: "ok"}`
5. You can type in certain paths to the end of the URL. Add the word scan so that the URL now ends with ```/api/scan```
 You should see a JSON response representing the results of a table scan.

### Web Application
A single-page static web app is provided for you. 
 * https://amazon-dynamodb-labs.com/static/global-serverless-application/web/index.html
 * This app allows you to enter one or more API endpoints, and stores each one as a browser cookie.  
 * The stored API endpoints will remain in the browser even if the backend were to have problems.  
 * In this way, the web app could make decisions about routing itself to an alternate API if there are errors or no response from the API being used.  
 * The web app does not contain any AWS code nor credentials, it simply makes HTTP GET calls to the API for you.
* The app's web content can be hosted from an S3 bucket, made globally available via Cloudfront, saved locally within Chrome, or converted into a mobile app. For this workshop we assume the user always has access to the web app even if the backend services become unavailable.

Steps:
1. Within the web app, press the **Add API** button.  
2. Paste in the API URL you created previously and click OK.
3. Review the buttons that appear. Click Ping to generate a request to the base level URL. 
The round trip latency will be displayed.  This may be slower than expected do to a Lambda cold start. 
Click Ping again and check the latency.
4. Click the **get-item** button. This will return the bookmark for user100 watching a show called AshlandValley.
5. Click the forward and back buttons. They will generate requests to increment or decrement the bookmark by 1 second.

You now have a test harness where you can perform reads and writes to a DynamoDB record via the custom API.

### Deploy the service stack to the second region, Ireland
1. Run the following instruction to instruct Chalice to deploy into eu-west-1 for our second region.
```bash 
export AWS_DEFAULT_REGION=eu-west-1
``` 

2. Run the following instruction and wait for the infrastructure to be created in eu-west-1.
```bash
chalice deploy
```
3. When the script completes, it reports a list of resources deployed. Again, copy down the new REST API URL to a note for later use.
4. Return to the web app.
5. Click **Add API** again and paste in the new API URL. A second row of buttons appears in an alternate color.

Note: In this workshop you have permissions for Global Tables in `us-west-2` and `eu-west-1`.
In your own account you could add any number of replicas in any regions.

Note 2: If you make any changes to the code in ```app.py```, you can push the updates to your Lambda function  
by running ```chalice deploy``` again.
