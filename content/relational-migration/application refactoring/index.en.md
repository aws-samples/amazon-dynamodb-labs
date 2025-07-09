---
title : "Application Refactoring"
weight : 40
---

## Updating the Client Application for DynamoDB
After you have chosen your DynamoDB table schema, and migrated any historical data over, 
you can consider what code changes are required so a new version of your app can call the DynamoDB 
read and write APIs.

The web app we have been using includes forms and buttons to perform standard CRUD (Create, Read, Update, Delete) operations.

The web app makes HTTP calls to the published API using standard GET and POST methods against certain API paths.

1. In Cloud9, open the left nav and locate the file **app.py**
2. Double click to open and review this file

In the bottom half of the file you will see several small handler functions that 
pass core read and write requests on to the **db** object's functions.


Notice the file contains a conditional import for the **db** object.

```python
if migration_stage == 'relational':
    from chalicelib import mysql_calls as db
else:
    from chalicelib import dynamodb_calls as db
```

