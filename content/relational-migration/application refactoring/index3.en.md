---
title : "Testing and reviewing DynamoDB code"
weight : 42
---

## Test drive your DynamoDB application

1. Click Tables to see a list of available tables in the account. You should see the 
Customers table, vCustOrders table, and a few other tables used by separate workshops.

3. Click on the Customers table, click the SCAN button to see the table's data.
4. Test the CRUD operations such as get-item, and the update and delete buttons in the data grid,
to make sure they work against the DynamoDB table.
4. Click on the Querying tab to display the form with GSI indexes listed.
5. On the idx_region GSI, enter 'North' and press GO.

![DynamoDB GSI Form](/static/images/relational-migration/ddb_gsi.png)

## Updating DynamoDB functions

Let's make a small code change to demonstrate the process to customize the DynamoDB functions.

6. In Cloud9, left nav, locate the chalicelib folder and open it.
7. Locate and open the file dynamodb_calls.py
8. Search for the text ```get_request['ConsistentRead'] = False```
9. Update this from False to True and click File/Save to save your work.
10. In the terminal prompt, redeploy:  

```bash
chalice deploy --stage dynamodb
```

11. Return to the web app, click on the Customers table, and enter cust_id value "0001" and click the GET ITEM button.
12. Verify a record was retrieved for you. This record was found using a strongly consistent read.
13. Feel free to extend the DynamoDB code to add new functions or modify existing ones.

