---
title : "DynamoDB-ready middle tier"
weight : 41
---

## Deploy a new DynamoDB-ready API

If you recall, we had run the command ```chalice deploy --stage relational``` previously 
to create the MySQL-ready middle tier.

We can repeat this to create a new API Gateway and Lambda stack, this time using the DynamoDB stage.

1. Within the Cloud9 terminal window, run:
```bash
chalice deploy --stage dynamodb
```
2. When this completes, find the new Rest API URL and copy it.
3. You can paste this into a new browser tab to test it. You should see a status message indicating 
the DynamoDB version of the API is working.

We now need a separate browser to test out the full web app experience, since
the original browser has a cookie set to the relational Rest API.

4. If you have multiple browsers on your laptop, such as Edge, Firefox, or Safari, 
open a different browser and navigate to the web app:

[https://amazon-dynamodb-labs.com/static/relational-migration/web/index.html](https://amazon-dynamodb-labs.com/static/relational-migration/web/index.html).

(You can also open the same browser in Incognito Mode for this step.)

5. Click the Target API button and paste in the new Rest API URL.
6. Notice the title of the page has updated to **DynamoDB App** in a blue color.
