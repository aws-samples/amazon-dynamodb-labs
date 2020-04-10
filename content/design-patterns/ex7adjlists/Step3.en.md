+++
title = "Step 3 - Query the table's invoice details"
date = 2019-12-02T12:24:34-08:00
weight = 3
+++

Run the following script to query the table’s invoice details.

```bash
python query_invoiceandbilling.py InvoiceAndBills 'I#1420'
```

Here's a look at the output.

```txt
=========================================================
 Invoice ID:I#1420, BillID:B#2485, BillAmount:$135,986.00 , BillBalance:$28,322,352.00

 Invoice ID:I#1420, BillID:B#2823, BillAmount:$592,769.00 , BillBalance:$8,382,270.00

 Invoice ID:I#1420, Customer ID:C#1420

 Invoice ID:I#1420, InvoiceStatus:Cancelled, InvoiceBalance:$28,458,338.00 , InvoiceDate:10/31/17, InvoiceDueDate:11/20/17
 =========================================================
```

Review the invoice details, customer details, and bill details. Notice how the results show the relationships between invoice ID, customer ID, and bill ID entities.
