---
title: "Simulate Order Updates"
date: 2023-12-01T00:00:00-00:00
weight: 125
chapter: false
---

After creating the Orders table, you uploaded some sample orders to the table. Lets explore the items on the Orders table before simulating any updates to any orders on the table.

Navigate to the DynamoDB Service page using the AWS Management Console. 

Select the **Orders** table then select the **Explore table items** button to view the orders on the table. 

See the :link[Viewing Table Data]{href="/hands-on-labs/explore-console/console-read-data"} section of the Hands-on Labs for Amazon DynamoDB if you need a refresher on exploring table items using the AWS Management Console.

There will be 4 orders on the table all having a status of **PLACED** as shown in the image below.

![Orders Table Items](/static/images/change-data-capture/ex1/orders-initial.png)

Feel free to explore the content of each order by selecting the **id** of the item using the DynamoDB Console.

There will be no data on the **OrdersHistory** table at this point beacuse no data has been written to it.

Copy the JSON data below into a file called **6421680-items.json**.

```bash
{
	":val2": {
		"S": "COMPLETE"
	},
	":val1": {
		"L": [
			{
				"M": {
					"id": {
						"S": "23769901"
					},
					"name": {
						"S": "Hydrating Face Cream"
					},
					"price": {
						"S": "£12.00"
					},
					"quantity": {
						"S": "8"
					},
					"status": {
						"S": " COMPLETE"
					}
				}
			},
			{
				"M": {
					"id": {
						"S": "23673445"
					},
					"name": {
						"S": "EXTRA Repair Serum"
					},
					"price": {
						"S": "£10.00"
					},
					"quantity": {
						"S": "5"
					},
					"status": {
						"S": " COMPLETE"
					}
				}
			}
		]
	}
}
```

In the json file you just created, the status of the items on the order and the status of the order are set as **COMPLETE**. Apply the update to order ID **6421680** using the command below. 

```bash
aws dynamodb update-item \
    --table-name Orders \
    --key '{ "id": {"S": "6421680"} }' \
    --update-expression "SET #items = :val1, #status = :val2" \
    --expression-attribute-names '{ "#items": "items", "#status": "status" }' \
    --expression-attribute-values file://6421680-items.json \
    --return-values ALL_NEW \
    --return-consumed-capacity TOTAL \
    --return-item-collection-metrics SIZE >> output.log
```

The output should be similar to the one below.

```json
{
    "Attributes": {
        "orderDate": {
            "S": "2023-10-01 20:39:08"
        },
        "shipDate": {
            "S": "2023-10-04 16:29:36"
        },
        "status": {
            "S": "COMPLETE"
        },
        "customer": {
            "M": {
                "name": {
                    "S": "Brody Dent"
                },
                "id": {
                    "S": "558490551"
                },
                "address": {
                    "S": "3 Bailey Lane, Clenchwarton,PE34 4AY"
                },
                "phone": {
                    "S": "+441268381612"
                }
            }
        },
        "id": {
            "S": "6421680"
        },
        "items": {
            "L": [
                {
                    "M": {
                        "name": {
                            "S": "Hydrating Face Cream"
                        },
                        "id": {
                            "S": "23769901"
                        },
                        "quantity": {
                            "S": "8"
                        },
                        "price": {
                            "S": "£12.00"
                        },
                        "status": {
                            "S": " COMPLETE"
                        }
                    }
                },
                {
                    "M": {
                        "name": {
                            "S": "EXTRA Repair Serum"
                        },
                        "id": {
                            "S": "23673445"
                        },
                        "quantity": {
                            "S": "5"
                        },
                        "price": {
                            "S": "£10.00"
                        },
                        "status": {
                            "S": " COMPLETE"
                        }
                    }
                }
            ]
        }
    },
    "ConsumedCapacity": {
        "TableName": "Orders",
        "CapacityUnits": 1.0
    }
}
```

Now explore the **Orders** and **OrdersHistory** tables to see the effects item update you performed.

The status of order ID 6421680 on the **Orders** table should be **COMPLETE** as shown in the image below.

![Orders Table Items](/static/images/change-data-capture/ex1/order-update-one.png)

... and there should be a single record on the **OrdersHistory** showing the previous state of order ID 6421680.

![OrdersHistory Table Items](/static/images/change-data-capture/ex1/orders-history-one.png)

Create two **expression attribute value** files named **4514280-complete-items.json** and **4514280-returned-items.json** using the JSON objects below. 

```json
{
  ":val1": {
    "L": [
      {
        "M": {
          "id": {
            "S": "23884750"
          },
          "name": {
            "S": "Metallic Long-Wear Cream Shadow"
          },
          "price": {
            "S": "£15.00"
          },
          "quantity": {
            "S": "13"
          },
          "status": {
            "S": "COMPLETE"
          }
        }
      },
      {
        "M": {
          "id": {
            "S": "23699354"
          },
          "name": {
            "S": "Eye Liner"
          },
          "price": {
            "S": "£9.00"
          },
          "quantity": {
            "S": "8"
          },
          "status": {
            "S": "COMPLETE"
          }
        }
      },
      {
        "M": {
          "id": {
            "S": "23599030"
          },
          "name": {
            "S": "Bronzing Powder"
          },
          "price": {
            "S": "£12.00"
          },
          "quantity": {
            "S": "10"
          },
          "status": {
            "S": "COMPLETE"
          }
        }
      }
    ]
  },
  ":val2": {
    "S": "COMPLETE"
  }
}
```

and

```json
{
  ":val1": {
    "L": [
      {
        "M": {
          "id": {
            "S": "23884750"
          },
          "name": {
            "S": "Metallic Long-Wear Cream Shadow"
          },
          "price": {
            "S": "£15.00"
          },
          "quantity": {
            "S": "13"
          },
          "status": {
            "S": "COMPLETE"
          }
        }
      },
      {
        "M": {
          "id": {
            "S": "23699354"
          },
          "name": {
            "S": "Eye Liner"
          },
          "price": {
            "S": "£9.00"
          },
          "quantity": {
            "S": "8"
          },
          "status": {
            "S": "RETURNED"
          }
        }
      },
      {
        "M": {
          "id": {
            "S": "23599030"
          },
          "name": {
            "S": "Bronzing Powder"
          },
          "price": {
            "S": "£12.00"
          },
          "quantity": {
            "S": "10"
          },
          "status": {
            "S": "RETURNED"
          }
        }
      }
    ]
  },
  ":val2": {
    "S": "COMPLETE"
  }
}
```

Perform additional updates for order ID **4514280** on the Orders table. This time first change the status of the order to **COMPLETE** then alter the status of some items on the same order to **RETURNED** using the commands below.

```bash
aws dynamodb update-item \
    --table-name Orders \
    --key '{ "id": {"S": "4514280"} }' \
    --update-expression "SET #items = :val1, #status = :val2" \
    --expression-attribute-names '{ "#items": "items", "#status": "status" }' \
    --expression-attribute-values file://4514280-complete-items.json \
    --return-values ALL_NEW \
    --return-consumed-capacity TOTAL \
    --return-item-collection-metrics SIZE >> output.log
```

Followed by

```bash
aws dynamodb update-item \
    --table-name Orders \
    --key '{ "id": {"S": "4514280"} }' \
    --update-expression "SET #items = :val1, #status = :val2" \
    --expression-attribute-names '{ "#items": "items", "#status": "status" }' \
    --expression-attribute-values file://4514280-returned-items.json \
    --return-values ALL_NEW \
    --return-consumed-capacity TOTAL \
    --return-item-collection-metrics SIZE >> output.log
```

Explore the items on the Orders and OrdersHistory tables to see the result of your updates.

The status of order ID 4514280 on the Orders table should be **COMPLETE** as shown in the image below.

![Orders Table Items](/static/images/change-data-capture/ex1/orders-update-two.png)

... and there should be two entries for order ID 4514280 on the OrdersHistory table showing the previous states of the order.

![OrdersHistory Table Items](/static/images/change-data-capture/ex1/orders-history-two.png)

::alert[**Note:** The order of updates to the Orders table is preserved by DynamoDB streams when changes are sent to the create order history lambda function. Since items on the OrdersHistory table have a sort key - sk, that is a timestamp, items on the OrderHistory table can be sorted in the order that they were created.]
