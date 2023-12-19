---
title: "Load Sample Data"
date: 2023-12-01T00:00:00-00:00
weight: 20
chapter: true
---

Copy the JSON data below in to a file named **Orders.json**.

```json
{ 
  "Orders": [ 
    { "PutRequest": { "Item": { "customer": { "M": { "id": { "S": "799102280" }, "name": { "S": "Salma Otero" }, "address": { "S": "22 Milton Road, Exeter,EX2 6BN" }, "phone": { "S": "+441482133202" } } }, "id": { "S": "4514280" }, "status": { "S": "PLACED" }, "items": { "L": [ { "M": { "id": { "S": "23884750" }, "name": { "S": "Metallic Long-Wear Cream Shadow" }, "quantity": { "S": "13" }, "status": { "S": "PURCHASED" }, "price": { "S": "£15.00" } } }, { "M": { "id": { "S": "23699354" }, "name": { "S": "Eye Liner" }, "quantity": { "S": "8" }, "status": { "S": "PURCHASED" }, "price": { "S": "£9.00" } } }, { "M": { "id": { "S": "23599030" }, "name": { "S": "Bronzing Powder" }, "quantity": { "S": "10" }, "status": { "S": "PURCHASED" }, "price": { "S": "£12.00" } } } ] }, "orderDate": { "S": "2023-10-01 01:05:54" }, "shipDate": { "S": "2023-10-04 18:54:12" } } } }, 
    { "PutRequest": { "Item": { "customer": { "M": { "id": { "S": "941852721" }, "name": { "S": "Taylor Burnette" }, "address": { "S": "31 Walkhampton Avenue, Bradwell Common,MK13 8ND" }, "phone": { "S": "+441663724681" } } }, "id": { "S": "9844720" }, "status": { "S": "PLACED" }, "items": { "L": [ { "M": { "id": { "S": "24002126" }, "name": { "S": "Shimmer Wash Eye Shadow" }, "quantity": { "S": "10" }, "status": { "S": "PURCHASED" }, "price": { "S": "£13.00" } } }, { "M": { "id": { "S": "23607685" }, "name": { "S": "Buffing Grains for Face" }, "quantity": { "S": "11" }, "status": { "S": "PURCHASED" }, "price": { "S": "£8.00" } } } ] }, "orderDate": { "S": "2023-10-01 01:49:13" }, "shipDate": { "S": "2023-10-06 13:05:33" } } } }, 
    { "PutRequest": { "Item": { "customer": { "M": { "id": { "S": "558490551" }, "name": { "S": "Brody Dent" }, "address": { "S": "3 Bailey Lane, Clenchwarton,PE34 4AY" }, "phone": { "S": "+441268381612" } } }, "id": { "S": "6421680" }, "status": { "S": "PLACED" }, "items": { "L": [ { "M": { "id": { "S": "23769901" }, "name": { "S": "Hydrating Face Cream" }, "quantity": { "S": "8" }, "status": { "S": "PURCHASED" }, "price": { "S": "£12.00" } } }, { "M": { "id": { "S": "23673445" }, "name": { "S": "EXTRA Repair Serum" }, "quantity": { "S": "5" }, "status": { "S": "PURCHASED" }, "price": { "S": "£10.00" } } } ] }, "orderDate": { "S": "2023-10-01 20:39:08" }, "shipDate": { "S": "2023-10-04 16:29:36" } } } }, 
    { "PutRequest": { "Item": { "customer": { "M": { "id": { "S": "242903240" }, "name": { "S": "Julia Caswell" }, "address": { "S": "81 Alwyn Road, Darlington,DL3 0AS" }, "phone": { "S": "+441305066386" } } }, "id": { "S": "9953371" }, "status": { "S": "PLACED" }, "items": { "L": [ { "M": { "id": { "S": "23924636" }, "name": { "S": "Protective Face Lotion" }, "quantity": { "S": "9" }, "status": { "S": "PURCHASED" }, "price": { "S": "£3.00" } } }, { "M": { "id": { "S": "23514506" }, "name": { "S": "Nail File" }, "quantity": { "S": "13" }, "status": { "S": "PURCHASED" }, "price": { "S": "£11.00" } } }, { "M": { "id": { "S": "23508704" }, "name": { "S": "Kitten Heels Powder Finish Foot Creme" }, "quantity": { "S": "10" }, "status": { "S": "PURCHASED" }, "price": { "S": "£11.00" } } } ] }, "orderDate": { "S": "2023-10-01 00:21:53" }, "shipDate": { "S": "2023-10-05 11:48:21" } } } } 
  ]
}
```

Load the sample data into the Orders table using the **batch-write-item** AWS CLI command.

```bash
aws dynamodb batch-write-item --request-items file://Orders.json
```

A successful load should produce a message similar to the one below.

#### Sample output
![sample-json](/static/images/change-data-capture/overview/load-data.png)
