+++
title = "Modifying Data"
date = 2020-04-21T07:38:58-05:00
weight = 34
+++

**Inserting Data**

The DynamoDB [PutItem API](https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_PutItem.html) is used to create a new item or to replace existing items completely with a new item.  It is invoked using the [put-item CLI command](https://docs.aws.amazon.com/cli/latest/reference/dynamodb/put-item.html).

Let's say we wanted to insert a new item into the *Reply* table from the console.  First, navigate to the **Reply** table click the **Create Item** button.

![Console Create Item 1](/images/hands-on-labs/explore-console/console_create_item_1.png)

You will need to click **Add new attribute** a couple of times to make some new String attributes, and then fill in the following data, then click **Create Item**.

```json
        "Id" : "Amazon DynamoDB#DynamoDB Thread 2",
        "ReplyDateTime" : "2021-04-27T17:47:30Z",
        "Message" : "DynamoDB Thread 2 Reply 3 text",
        "PostedBy" : "User C"
```

![Console Create Item 2](/images/hands-on-labs/explore-console/console_create_item_2.png)

**Updating or Deleting Data**

The DynamoDB [UpdateItem API](https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_UpdateItem.html) is used to create a new item or to replace existing items completely with a new item.  It is invoked using the [update-item CLI command](https://docs.aws.amazon.com/cli/latest/reference/dynamodb/update-item.html).  This API requires you to specify the full Primary Key and can selectively modify specific attributes without changing others(you don't need to pass in the full item).

The DynamoDB [DeleteItem API](https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_DeleteItem.html) is used to create a new item or to replace existing items completely with a new item.  It is invoked using the [delete-item CLI command](https://docs.aws.amazon.com/cli/latest/reference/dynamodb/delete-item.html).

You can easily modify or delete an item using the console by selecting the checkbox next to the item of interest, clicking the **Actions** dropdown and performing the desired action.

![Console Delete Item](/images/hands-on-labs/explore-console/console_delete_item.png)

**Exercise**

Update the ProductCatalog item where Id=201 to add new colors "Silver" and "Green" to the list of colors for that bike type.  Then use the Item Editor again to remove those "Silver" and "Green" list entries to return it to the original state.

The solution is expandable below but try to figure it out yourself before moving forward.

**Click below to expand and see the exercise solutions**

{{%expand "Expand this to see the solution" %}}

Navigate to the **ProductCatalog** Table and click the `Id` 201 hyperlink to bring up the Item Editor for that item. Click the `+` icon next to the *Color* attribute to expand that List.

![Console Modify Item 1](/images/hands-on-labs/explore-console/console_modify_item_1.png)

Click `Insert a field` and pick the `String` type.  Do this twice.  Add the colors "Silver" and "Green" to the list, then click `Save changes`.

![Console Modify Item 2](/images/hands-on-labs/explore-console/console_modify_item_2.png)

We can see by expanding the Items Preview that those two list entries were added.

![Console Modify Item 3](/images/hands-on-labs/explore-console/console_modify_item_3.png)

Return to the item editor for `Id` 201 and use the `Remove` button next to the Silver and Green list entries to remove them from the `Color` attribute, then click `Save changes`.

![Console Modify Item 4](/images/hands-on-labs/explore-console/console_modify_item_4.png)

{{% /expand%}}
