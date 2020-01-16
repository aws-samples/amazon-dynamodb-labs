+++
title = "Step 4 - Query the Customer details and Bill details using the Index"
date = 2019-12-02T12:24:34-08:00
weight = 4
+++

Query using the Customer ID, and review the output showing the Customer details, and the list of related Invoice(s). Notice how the output shows all the Invoices associated with the customer.
```py
python query_index_invoiceandbilling.py InvoiceAndBills 'C#1249'
```
Query using the Bill ID, and review the output showing the Bill details, and the details of the associated Invoice(s).
```py
python query_index_invoiceandbilling.py InvoiceAndBills 'B#3392'
```
