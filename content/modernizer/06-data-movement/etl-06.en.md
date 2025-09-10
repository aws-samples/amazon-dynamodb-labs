---
title: "6.6 Data Movement"
menuTitle: "Data Movement"
date: 2025-09-02T16:43:04-05:00
weight: 36
chapter: false
---

Now comes the most exciting part - actually testing your migration system with real user actions! You'll see firsthand how the feature flag system controls where data goes, and you'll prove that your migration from MySQL to DynamoDB actually works.

This is your test flight - you want to see all the systems working together before you declare the mission successful.

### Monitoring the Migration Process

When you use the admin portal to toggle feature flags, you're actually calling REST API endpoints that control your application's database behavior. The system logs every phase change so you can track what's happening.

![Migration control panel](/static/images/modernizer/6/stage06-26.png)

These log messages are crucial for understanding:
- **When** changes happen (timestamps for troubleshooting)
- **What** changed (which flags were modified)
- **Who** made the change (accountability for production systems)
- **Current State** (confirmation of the new configuration)

This logging gives you a complete audit trail of your migration process.

## Testing Phase 2: Dual Write + MySQL Read

Keep two browser tabs open:
- **Tab 1**: The migration control admin portal 
- **Tab 2**: The online shopping store application

This setup lets you control the migration and immediately test the results.

While in Phase 2 (dual write + MySQL read), go to the shopping store and add an item to your cart.

![Migration control panel](/static/images/modernizer/6/stage06-27.png)

What happens behind the scenes:
- **Write Operation**: The system writes the cart item to BOTH MySQL and DynamoDB
- **Read Operation**: When the page loads your cart, it reads ONLY from MySQL
- **User Experience**: You see the item in your cart normally
- **Data Flow**: Data flows to both databases, but the app still trusts MySQL

Check the MySQL database first. Look at the user views you created earlier - you should see the new cart item for the admin user.

![Migration control panel](/static/images/modernizer/6/stage06-28.png)

This confirms the MySQL write operation worked correctly, your existing database is still receiving updates and the application can still function normally if you need to roll back.

Now check the AWS DynamoDB console. Open the `Users` table and look for the admin user's record - you should see the same cart item there too.

![Migration control panel](/static/images/modernizer/6/stage06-29.png)

This proves the dual-write system is working correctly, data transformation from MySQL to DynamoDB format is working, both databases now have the same information, you're ready to start reading from DynamoDB.

## Testing Phase 5: DynamoDB Only

Now for the big test! Go back to the migration control panel and switch directly to Phase 5 (DynamoDB Only). This simulates completing the entire migration process instantly.

In Phase 5:
- **READ_MYSQL**: OFF (no reading from MySQL)
- **READ_DDB**: ON (all reads come from DynamoDB)  
- **WRITE_MYSQL**: OFF (no writing to MySQL)
- **WRITE_DDB**: ON (all writes go to DynamoDB)

Go back to your shopping cart and complete the checkout process for the item you added earlier.

![Migration control panel](/static/images/modernizer/6/stage06-30.png)

This transaction is critical because it:
- **Reads** your cart data from DynamoDB (not MySQL)
- **Processes** the checkout using DynamoDB data
- **Writes** the order information only to DynamoDB
- **Deletes** the cart item from DynamoDB only

Refresh the DynamoDB Users table and look for changes in the admin user's record. You should see:

- **Cart Item Gone**: The `CART#1` item has disappeared
- **New Order Created**: A new `ORDER#` record has appeared
- **Complete Transaction**: The checkout process worked entirely with DynamoDB

![Migration control panel](/static/images/modernizer/6/stage06-31.png)

This proves that your application can:
- Read complex data from DynamoDB correctly
- Process business logic with NoSQL data
- Write new records in the proper DynamoDB format
- Delete records when needed

Finally, check your MySQL user views. You should NOT see the completed order there, because in Phase 5, the application doesn't write to MySQL anymore.

![Migration control panel](/static/images/modernizer/6/stage06-32.png)

This confirms the Phase 5 configuration is working correctly, your application is truly running on DynamoDB, MySQL is no longer part of your active system and the migration is functionally complete.

## What You've Accomplished

Congratulations! You have successfully migrated your application from MySQL to DynamoDB. Your test proves that:

- **Data Migration Works**: Your historical data was correctly transferred from MySQL to DynamoDB using the ETL process.
- **Application Logic Works**: Your business logic (shopping cart, checkout process) works correctly with NoSQL data.
- **Performance Is Acceptable**: The application responds normally when reading and writing DynamoDB data.
- **Feature Flags Work**: You can control database usage precisely through the admin portal.
- **Rollback Is Possible**: Until Phase 5, you could have rolled back to MySQL at any time.

### Technical Achievement

You've built and operated a dual-database system that safely migrated data without downtime, provides complete control over the migration process, validates data consistency between systems and work a the same time with MySQL and DynamoDB.

Your application is now successfully running on DynamoDB, with all the benefits of NoSQL scalability, performance, and cost-effectiveness. The modernization project is complete!
