---
title : "Chalice API"
weight : 17
---

### Application Setup

We will be deploying a new application stack using [AWS Chalice](https://github.com/aws/chalice),
a Python-based serverless framework. 

Chalice deploys the following components:

* An **AWS Lambda function** to perform database read and write calls
* An **Amazon API Gateway service** with integration to the Lambda function
* Associated roles and permissions

In this workshop, we will focus on the AWS Lambda source code.

::alert[Chalice allows us to run unit tests against this code locally, before deploying to Lambda, and further allows for a mock deployment to localhost:8000 in case you wish to launch the web service privately, from your laptop.]{header="Note"}

The Lambda source code project has been setup as follows
* Entry point : **app.py** 
* Read and write function implementations: 
  * **chalicelib/mysql_calls.py**
  * **chalicelib/dynamodb_calls.py**


1. Next, let's deploy the Chalice application stack. This step may take a few minutes to complete. 

```bash
chalice deploy --stage relational
```

2. The script will create resources and provide details of the new stack. Notice the Rest API URL value.
   This is the public endpoint for the middle-tier service we will use to drive the
   sample relational application.
3. Carefully copy the Rest API URL value.
4. Optional: Paste this into a new browser tab to test it. You should see a status message appear.

---

## Single Page Web App
A single-page web application is included in the /webapp project folder.
The web app has already been deployed for you in a public S3 bucket for convenience. 

5. Navigate to [https://amazon-dynamodb-labs.com/static/relational-migration/web/index.html](https://amazon-dynamodb-labs.com/static/relational-migration/web/index.html)

The webapp stores the API URL you provide as a browser cookie.
    Then, Javascript functions will call the API for you, when you click on
    various buttons in the app.

6. Click the "Target API" button and paste in the API you generated in step 1.
7. Click the "Tables" button. A list of tables might appear below the button, however none exist yet.
    We will be creating sample tables in the next step. 





