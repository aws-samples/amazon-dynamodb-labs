---
title : "Generate Table Definition in a script"
weight : 24
---

## mysql_desc_ddb.py

1. In the command prompt, type ```ls``` to review the scripts available to you.

2. The **mysql_desc_ddb.py** script will generate a table definition for you as we saw in the web app.

3. Run 
```bash 
python3 mysql_desc_ddb.py Customers
```

You should see the same table definition including any GSIs if there were indexes on the base table.





