---
title: "6.5 Admin Portal"
menuTitle: "Admin Portal"
date: 2025-09-02T16:43:04-05:00
weight: 35
chapter: false
---

Now that your data has been successfully migrated to DynamoDB, it's time to access the admin portal that controls your feature flag system from Stage 5. You need special administrator access to safely control the migration between databases.

The admin portal is where you'll manage the transition from MySQL-only operation to DynamoDB-only operation through the 5 migration phases you learned about in Stage 5.

### What Is Super Admin Access?

The migration control system is too powerful to let just anyone access it. Imagine if any employee could decide to switch your entire company's database system on a whim! That's why the system requires "super admin" privileges.

In your user database, there's a special field called `super_admin` that acts like a VIP pass. When this field is set to `1` (true) for a user, it means they have permission to: View the hidden migration control panel, switch between migration phases, control individual feature flags, monitor the dual-database validation system and make critical decisions about your database migration.

There's a small issue we need to fix first. During the data modeling process in Stage 2, the `super_admin` field wasn't included in the migration contract. This means the MySQL views don't include this field and the DynamoDB tables don't have this attribute. In other words no users currently have admin access to the migration panel, we need to manually add this field to both databases so you can access the control panel.

## Setting Up Admin Access

### Step 1: Update MySQL Database

First, we'll give the `admin` user super admin privileges in the MySQL database, using the MySQL MCP Server:

```shell
Could you please use the MySQL MCP server to update the `admin` user from the Users table and set the attribute `super_admin` to 1?
```

![Migration control panel](/static/images/modernizer/6/stage06-23.png)

The MCP server will first retrieve the user information, then apply the update.

### Step 2: Update DynamoDB Database

Next, we need to make the same change in DynamoDB so both databases have consistent information:

```shell
Could you please use the DynamoDB MCP server to update the `admin` user from the `Users` table and set the its attribute `super_admin` value to 1?
```

![Migration control panel](/static/images/modernizer/6/stage06-24.png)

This ensures that:
- Both databases have the same user permissions
- The dual-database validation system won't report inconsistencies
- The admin user will have access regardless of which database the application is reading from

### Why Both Databases?

You might wonder why we need to update both databases. Remember, your application can be reading from MySQL, DynamoDB, or both depending on your current migration phase. If the `super_admin` field is missing from either database, the admin user might lose access when you switch phases.

## Accessing the Migration Control Panel

### Step 3: Navigate to the Admin Portal

Once both database updates are complete, you can access the hidden admin portal at `[your-url]/store/admin/migration-control`

This URL isn't linked anywhere in your normal application - it's a hidden page that only super administrators know about.

### Step 4: Administrator Authentication

The first time you access the admin portal, you'll need to log in with administrator credentials. The system will:

- Verify that you're logged in as a valid user
- Check that your user account has `super_admin = 1` in the database
- Grant access to the migration control interface
- Remember your admin session for future visits

If you don't have super admin privileges, you'll see an "Access Denied" message instead of the control panel.

### Step 5: Begin Controlled Migration

Once you're in the admin portal, you'll see the migration control interface with options to:

- **View Current Status**: See which migration phase you're currently in
- **Switch Phases**: Move between the 5 migration phases safely
- **Monitor Validation**: Check how well the dual-database system is working
- **Control Individual Flags**: Fine-tune the feature flags for testing

## Your First Modernization Step

Now that you have access to the control panel, you can take your first step in the controlled migration process. Click the button to enable "Phase 2: Dual Write + MySQL Read".

![Migration control panel](/static/images/modernizer/6/stage06-25.png)

This phase is the first safe step in your migration because it:
- **Keeps Reading from MySQL**: Your application continues to serve data from the reliable MySQL database
- **Starts Writing to Both**: Every new data change goes to both MySQL and DynamoDB
- **Maintains Performance**: Users don't notice any difference in application speed
- **Builds Confidence**: You can monitor that DynamoDB writes are working correctly

With the admin portal working and Phase 2 enabled, you've taken the first step in your controlled migration from MySQL to DynamoDB. Your application is now writing to both databases while still serving data from the reliable MySQL system, giving you the foundation to safely continue the migration process.
