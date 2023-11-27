---
title: "Viewing Table Data"
date: 2020-04-21T07:38:58-05:00
weight: 31
---

First, go to the [DynamoDB Console](https://console.aws.amazon.com/dynamodbv2/) and click on *Tables* from the side menu.

![Console Pick Tables](/static/images/hands-on-labs/explore-console/dynamodb_pick_tables.png)

Next, choose the `ProductCatalog` table and click `Explore table items` on the top right to view the items.

![Console ProductCatalog Items Preview](/static/images/hands-on-labs/explore-console/console_productcatalog_preview.png)

We can see visually that the table has a Partition Key of *Id* (which is the `Number` type), no sort key, and there are 8 items in the table.  Some items are Books and some items are Bicycles and some attributes like *Id*, *Price*, *ProductCategory*, and *Title* exist in every Item while other Category specific attributes like Authors or Colors exist only on some items.

Click on the *Id* attribute `101` to pull up the Item editor for that Item.  We can see and modify all the attributes for this item right from the console.  Try changing the *Title* to "Book 101 Title New and Improved".  Click **Add new attribute** named *Reviewers* of the String set type and then clicking **Insert a field** twice to add a couple of entries to that set.  When you're done click **Save changes**

![Console ProductCatalog Items Editor Forms](/static/images/hands-on-labs/explore-console/console_item_editor_forms.png)

You can also use the Item editor in DynamoDB JSON notation (instead of the default Form based editor) by clicking **JSON** in the top right corner. This notation should look familiar if you already went through the [Explore the DynamoDB CLI](/hands-on-labs/explore-cli.html) portion of the lab. The DynamoDB JSON format is described in the [DynamoDB Low-Level API](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Programming.LowLevelAPI.html) section of the Developer Guide.

![Console ProductCatalog Items Editor JSON](/static/images/hands-on-labs/explore-console/console_item_editor_json.png)
