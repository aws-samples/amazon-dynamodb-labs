+++
title = "Step 4 - Query the Customer details and Bill details using the Index"
date = 2019-12-02T12:24:34-08:00
weight = 4
+++

Query using the customer ID, and review the output showing the customer details and the list of related invoices. Notice how the output shows all the invoices associated with the customer.

```py
python query_index_invoiceandbilling.py InvoiceAndBills 'C#1249'
```
Now, query using the bill ID, and review the output showing the bill details and the details of the associated invoices.

```py
python query_index_invoiceandbilling.py InvoiceAndBills 'B#3392'
```
