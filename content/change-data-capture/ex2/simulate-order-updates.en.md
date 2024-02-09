---
title: "Simulate Order Updates"
date: 2023-12-01T00:00:00-00:00
weight: 225
chapter: false
---

Similar to the previous lab, lets perform item level updates to the **Orders** table and watch old copies of updated items get written to the **OrdersHistory**.

Navigate to the DynamoDB Service page using the AWS Management Console. 

Select the **Orders** table then select **Explore table items** button to view the orders on the table. 

See the :link[Viewing Table Data]{href="/hands-on-labs/explore-console/console-read-data"} section of the Hands-on Labs for Amazon DynamoDB if you need a refresher on exploring table items using the AWS Management Console.

The items on the table should look familiar from the previous lab. The status of items on the **Orders** table may vary if you performed additional simulations during the previous lab on change data capture using DynamoDB streams.  

![Orders Table Items](/static/images/change-data-capture/ex2/orders-lab2-initial.png)

Also explore the orders on the **OrdersHistory** table. The number of items on the table will depend on the number of updates you made to the Orders table during the previous lab.

Copy the JSON data below into a file called **9844720-items.json**.

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
						"S": "24002126"
					},
					"name": {
						"S": "Shimmer Wash Eye Shadow"
					},
					"price": {
						"S": "£13.00"
					},
					"quantity": {
						"S": "10"
					},
					"status": {
						"S": "COMPLETE"
					}
				}
			},
			{
				"M": {
					"id": {
						"S": "23607685"
					},
					"name": {
						"S": "Buffing Grains for Face"
					},
					"price": {
						"S": "£8.00"
					},
					"quantity": {
						"S": "11"
					},
					"status": {
						"S": "COMPLETE"
					}
				}
			}
		]
	}
}
```

Update the status of order ID **9844720** from **PLACED** to **COMPLETE** using the command below. 

```bash
aws dynamodb update-item \
    --table-name Orders \
    --key '{ "id": {"S": "9844720"} }' \
    --update-expression "SET #items = :val1, #status = :val2" \
    --expression-attribute-names '{ "#items": "items", "#status": "status" }' \
    --expression-attribute-values file://9844720-items.json \
    --return-values ALL_NEW \
    --return-consumed-capacity TOTAL \
    --return-item-collection-metrics SIZE > output.log
```

The output should be similar to the one below.

```json
{
    "Attributes": {
        "orderDate": {
            "S": "2023-10-01 01:49:13"
        },
        "shipDate": {
            "S": "2023-10-06 13:05:33"
        },
        "status": {
            "S": "COMPLETE"
        },
        "customer": {
            "M": {
                "name": {
                    "S": "Taylor Burnette"
                },
                "id": {
                    "S": "941852721"
                },
                "address": {
                    "S": "31 Walkhampton Avenue, Bradwell Common,MK13 8ND"
                },
                "phone": {
                    "S": "+441663724681"
                }
            }
        },
        "id": {
            "S": "9844720"
        },
        "items": {
            "L": [
                {
                    "M": {
                        "name": {
                            "S": "Shimmer Wash Eye Shadow"
                        },
                        "id": {
                            "S": "24002126"
                        },
                        "quantity": {
                            "S": "10"
                        },
                        "price": {
                            "S": "£13.00"
                        },
                        "status": {
                            "S": "COMPLETE"
                        }
                    }
                },
                {
                    "M": {
                        "name": {
                            "S": "Buffing Grains for Face"
                        },
                        "id": {
                            "S": "23607685"
                        },
                        "quantity": {
                            "S": "11"
                        },
                        "price": {
                            "S": "£8.00"
                        },
                        "status": {
                            "S": "COMPLETE"
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

View the items on the **Orders** and **OrdersHistory** tables to see the effects of item update you performed.

The status of order ID **9844720** on the **Orders** table should be **COMPLETE** as shown in the image below.

![Orders Table Items](/static/images/change-data-capture/ex2/orders-update-one.png)

... and there should be a single record on the **OrdersHistory** showing the previous state of order ID **9844720**.

![OrdersHistory Table Items](/static/images/change-data-capture/ex2/orders-history-one.png)

Create two **expression attribute value** files named **9953371-active-items.json** and **9953371-cancelled-items.json** using the JSON objects below. 

```json
{
	":val1": {
    "L": [
      {
        "M": {
          "id": {
            "S": "23924636"
          },
          "name": {
            "S": "Protective Face Lotion"
          },
          "price": {
            "S": "£3.00"
          },
          "quantity": {
            "S": "9"
          },
          "status": {
            "S": "CANCELLED"
          }
        }
      },
      {
        "M": {
          "id": {
            "S": "23514506"
          },
          "name": {
            "S": "Nail File"
          },
          "price": {
            "S": "£11.00"
          },
          "quantity": {
            "S": "13"
          },
          "status": {
            "S": "PLACED"
          }
        }
      },
      {
        "M": {
          "id": {
            "S": "23508704"
          },
          "name": {
            "S": "Kitten Heels Powder Finish Foot Creme"
          },
          "price": {
            "S": "£11.00"
          },
          "quantity": {
            "S": "10"
          },
          "status": {
            "S": "PLACED"
          }
        }
      }
    ]
  },
	":val2": {
		"S": "ACTIVE"
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
            "S": "23924636"
          },
          "name": {
            "S": "Protective Face Lotion"
          },
          "price": {
            "S": "£3.00"
          },
          "quantity": {
            "S": "9"
          },
          "status": {
            "S": "CANCELLED"
          }
        }
      },
      {
        "M": {
          "id": {
            "S": "23514506"
          },
          "name": {
            "S": "Nail File"
          },
          "price": {
            "S": "£11.00"
          },
          "quantity": {
            "S": "13"
          },
          "status": {
            "S": "CANCELLED"
          }
        }
      },
      {
        "M": {
          "id": {
            "S": "23508704"
          },
          "name": {
            "S": "Kitten Heels Powder Finish Foot Creme"
          },
          "price": {
            "S": "£11.00"
          },
          "quantity": {
            "S": "10"
          },
          "status": {
            "S": "CANCELLED"
          }
        }
      }
    ]
  },
	":val2": {
		"S": "CANCELLED"
	}
}
```

Perform additional updates FOR order ID **9953371** on the Orders table. Start by changing the status of the order to **ACTIVE** then perform another update by setting the status of the same order to **CANCELLED** using the commands below.

```bash
aws dynamodb update-item \
    --table-name Orders \
    --key '{ "id": {"S": "9953371"} }' \
    --update-expression "SET #items = :val1, #status = :val2" \
    --expression-attribute-names '{ "#items": "items", "#status": "status" }' \
    --expression-attribute-values file://9953371-active-items.json \
    --return-values ALL_NEW \
    --return-consumed-capacity TOTAL \
    --return-item-collection-metrics SIZE > output.log
```

Followed by

```bash
aws dynamodb update-item \
    --table-name Orders \
    --key '{ "id": {"S": "9953371"} }' \
    --update-expression "SET #items = :val1, #status = :val2" \
    --expression-attribute-names '{ "#items": "items", "#status": "status" }' \
    --expression-attribute-values file://9953371-cancelled-items.json \
    --return-values ALL_NEW \
    --return-consumed-capacity TOTAL \
    --return-item-collection-metrics SIZE > output.log
```

Explore the items on the **Orders** and **OrdersHistory** tables to see the result of your updates. The status for order ID **9953371** should be updated on the Orders table and there should be two items on the OrdersHistory table for order ID **9953371**.

![Orders Table Items](/static/images/change-data-capture/ex2/orders-update-two.png)

... and there should be two entries for order ID **9953371** on the **OrdersHistory** table showing the previous states of the order.

![OrdersHistory Table Items](/static/images/change-data-capture/ex2/orders-history-two.png)

::alert[**Note:** The order of updates to the Orders table is not preserved by Kinesis Data streams when changes are sent to the create order history lambda function. If you need to record the sequence that updates were made to items on the Orders table, you can configure the precision of the ApproximateCreationDateTime for your Kinesis Data stream. Once this is done, stream records written to your Kinesis Data stream will have an approximate creation date time attribute that can be used to record the sequence of updates to items on the Orders table. See [How Kinesis Data Streams works with DynamoDB](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/kds.html#kds_howitworks) for more information on how it works.]
