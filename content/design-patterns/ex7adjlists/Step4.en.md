+++
title = "Step 4 - Query the Customer details and Bill details using the Index"
date = 2019-12-02T12:24:34-08:00
weight = 4
+++

Query using the customer ID, and review the output showing the customer details and the list of related invoices. Notice how the output shows all the invoices associated with the customer.

```bash
python query_index_invoiceandbilling.py InvoiceAndBills 'C#1249'
```

Here's a look at the output.

```txt

 =========================================================
 Invoice ID: I#661, Customer ID: C#1249


 Invoice ID: I#1249, Customer ID: C#1249
 =========================================================

```

Now, query using the bill ID, and review the output showing the bill details and the details of the associated invoices. Notice how the output shows all the invoices associated with a specific bill.

Run the following Python script:

```bash
python query_index_invoiceandbilling.py InvoiceAndBills 'B#3392'
```

Here's a look at the output.

```txt
=========================================================
 Invoice ID: I#506, Bill ID: B#3392, BillAmount: $383,572.00 , BillBalance: $5,345,699.00


 Invoice ID: I#1721, Bill ID: B#3392, BillAmount: $401,844.00 , BillBalance: $25,408,787.00


 Invoice ID: I#390, Bill ID: B#3392, BillAmount: $581,765.00 , BillBalance: $11,588,362.00
 =========================================================
```
