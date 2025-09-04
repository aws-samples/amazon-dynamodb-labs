---
title: "Stage 5: Application Refactoring"
date: 2025-09-02T15:41:04-05:00
weight: 30
chapter: true
---
::alert[In this workshop this stage has already been completed for you. Please review the artifacts available on `/artifacts/stage-05` ]{type="info"}

## Building the Control System for Your Migration

Stage 5 is where you build the actual control system that lets you safely switch between MySQL and DynamoDB. Think of this as building the cockpit controls for a spaceship - you need precise controls to navigate the transition from your old database system to the new one without crashing anything.

This stage takes the dual database abstraction layer from Stage 3 and the DynamoDB connectivity from Stage 4, then adds the **feature flag** API system that gives you complete control over your migration process.

## What You'll Build

You'll create a backend REST API system that controls how your application uses the databases through simple API calls. The system is designed so your frontend never needs to change - all the database switching happens behind the scenes through configuration.

The core of this system is a Feature Flag Controller that manages four boolean switches:

- **READ_MYSQL**: Should the app read from MySQL?
- **READ_DDB**: Should the app read from DynamoDB?
- **WRITE_MYSQL**: Should the app write to MySQL?
- **WRITE_DDB**: Should the app write to DynamoDB?

By turning these switches on and off in different combinations, you create the 5 migration phases that let you safely transition from MySQL to DynamoDB.

### Migration Control API Endpoints

You'll build REST API endpoints that give you remote control over your database migration:

- `GET /api/migration/status` - Check what phase you're currently in and see all flag settings
- `POST /api/migration/phase` - Jump to a specific migration phase (1 through 5)
- `PUT /api/migration/flags` - Manually control individual feature flags for custom configurations
- `GET /api/migration/validation` - Monitor how well the dual-read validation is working

### Phase Configuration System

The system automatically manages the 5 migration phases by setting the right combination of feature flags:

**Phase 1 - MySQL Only** (Your starting point)
- READ_MYSQL: ON, READ_DDB: OFF
- WRITE_MYSQL: ON, WRITE_DDB: OFF

**Phase 2 - Dual Write + MySQL Read** (Safety mode)
- READ_MYSQL: ON, READ_DDB: OFF
- WRITE_MYSQL: ON, WRITE_DDB: ON

**Phase 3 - Dual Write + Dual Read** (Validation mode)
- READ_MYSQL: ON, READ_DDB: ON
- WRITE_MYSQL: ON, WRITE_DDB: ON

**Phase 4 - Dual Write + DynamoDB Read** (Transition mode)
- READ_MYSQL: OFF, READ_DDB: ON
- WRITE_MYSQL: ON, WRITE_DDB: ON

**Phase 5 - DynamoDB Only** (Your end goal)
- READ_MYSQL: OFF, READ_DDB: ON
- WRITE_MYSQL: OFF, WRITE_DDB: ON

### Validation and Monitoring System

During phases 3 and 4 (when you're reading from both databases), the system automatically compares the results from MySQL and DynamoDB. This validation system:

- **Logs Differences**: Records any inconsistencies between the two databases
- **Tracks Success Rates**: Shows you how often the databases return matching results
- **Provides Error Details**: Gives you specific information about what didn't match
- **Monitors Performance**: Compares response times between MySQL and DynamoDB

### Frontend Transparency

One of the coolest parts of this system is that your frontend application never knows about the migration. All your existing API endpoints continue to work exactly the same way:

```javascript
// This code never changes during migration
const createUser = async (userData) => {
    const response = await fetch('/api/users', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(userData)
    });
    return response.json();
};
```

Behind the scenes, the backend automatically routes this request to MySQL, DynamoDB, or both databases based on your current migration phase, but the frontend never needs to know about it.

### Super Admin Control Panel

You'll also build a hidden web interface that lets authorized administrators control the migration through a browser instead of direct API calls. This admin panel:

- **Shows Current Status**: Displays which phase you're in and all flag settings
- **Provides Phase Buttons**: One-click switching between migration phases
- **Offers Manual Controls**: Individual checkboxes for fine-grained flag control
- **Displays Validation Data**: Shows success rates and error information
- **Requires Special Access**: Only users with super admin privileges can access it

## Controlling the Modernization

By controlling database operations through feature flags, you can move forward or backward through the migration phases instantly. If something goes wrong in Phase 4, you can immediately switch back to Phase 2 and be running safely on MySQL again.

Phases 3 and 4 let you test DynamoDB with real user traffic while still having MySQL as a safety net. You can see exactly how DynamoDB performs with your actual data and usage patterns before fully committing to it.

Since all the database switching happens through configuration changes and your frontend never changes, users never experience any downtime or disruption. They continue using your application normally while you're migrating the database underneath.

The API system gives you precise control over exactly how your application uses the databases. You can move through the phases step by step, or even create custom configurations for testing specific scenarios.

During dual-read phases, the system automatically validates that both databases are returning the same results, giving you confidence that your migration contract and data transformations are working correctly.

## Technical Implementation Details

The system extends your existing dual database abstraction layer to include the feature flag controller. Your business logic continues to use the same repository interfaces, but now the repository implementation checks the feature flags to decide which database(s) to use for each operation.

The system includes smart error handling - if DynamoDB operations fail during dual-write phases, the application continues using MySQL results so users never see errors. All DynamoDB failures are logged for investigation, but they don't break your application.

### Authentication and Authorization

The migration control APIs are protected by authentication middleware that requires super admin privileges. The system also includes user management functions to promote and demote users to/from super admin status.

You'll extend your existing user table with a `super_admin` boolean field to control access to the migration interface. The system includes migration scripts to safely add this field to your existing database.

## Building Your Migration Control System

This stage transforms your modernization project from a planning exercise into a live, controllable system. You'll have the tools to safely navigate the transition from MySQL to DynamoDB with complete confidence that you can handle any issues that arise.

The feature flag system gives you the power to migrate your database while keeping your application running smoothly for users, and the validation system ensures you catch any problems before they affect your production environment.

By the end of this stage, you'll have a system that can safely migrate your database while providing you with all the monitoring, control, and safety features you need for a successful modernization project.
