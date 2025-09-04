---
title: "Database Modernizr Workflow"
date: 2025-09-01T10:41:04-05:00
weight: 30
chapter: true
---

## Application Analysis and Baseline Establishment

Before beginning the modernization process, you must thoroughly understand the existing system architecture. This involves analyzing the current MySQL-based e-commerce application to identify all data access patterns, performance characteristics, and system dependencies.

Begin by reviewing the application documentation in the `README.md` file, which provides an overview of the system architecture and functionality.

::alert[You don't have to follow the `README.md` instructions as your environment is already pre-configured for you. ]{type="info"}

![README](/static/images/modernizr/1/workflow-01.png)

## Starting the Application Services

The e-commerce application follows a standard three-tier architecture:
1. **Backend Service** - Express.js API server handling business logic and database interactions
2. **Frontend Application** - React-based user interface for customer interactions
3. **MySQL Database** - Relational database storing all application data

You'll need to start both the backend and frontend services to establish a baseline for analysis.

### Initializing the Backend Service

The backend API server manages all client requests and database transactions. Navigate to the `/backend` directory and open an integrated terminal (right-click > "Open in Integrated Terminal"). Grant any requested permissions when prompted.

![menu](/static/images/modernizr/1/workflow-02.png)

Build and start the backend service using these commands:

```shell
npm run build
npm run start
```

Monitor the startup sequence output. A successful initialization will display output similar to:

```console
👤 DatabaseFactory.createUserRepository called
🔧 DynamoDBClientManager.getClient() called
👤 Creating UserDualWriteWrapper
🔐 AuthService repositories created
🛍️ ShoppingCartService constructor called
🛍️ ShoppingCartService repositories created
🛍️ ShoppingCartService constructor called
🛍️ ShoppingCartService repositories created
Starting server with enhanced error handling...
✅ Environment variables validated successfully
✅ Database abstraction layer initialized with mysql configuration
Registering routes...
All routes registered.
Server setup complete with comprehensive error handling
📝 Using MySQL-only mode (Phase 1)
🚀 Server is running on port 8100
📊 Health check: http://localhost:8100/api/health
🔧 Performance: http://localhost:8100/api/performance
📈 Metrics: http://localhost:8100/api/metrics
```

**Important:** Keep this terminal window open! If you close it, the backend service will stop working, and our application won't function properly.

### Launching the Frontend Application

Initialize the React frontend application by opening a terminal in the `/frontend` directory and executing:

```shell
npm run serve:prod
```

Allow several minutes for the build process to complete. Dismiss any popup notifications that may appear during startup.

## Application Verification and Analysis

With both services running, you can now interact with the complete application stack to understand its current behavior and performance characteristics.

### Backend Health Check

Verify the API server is responding correctly by accessing the health endpoint:

1. Copy your VS Code environment URL
2. Open a new browser tab
3. Navigate to `[your-url]/api/health`

This endpoint should return status information confirming the backend is operational:

![Backend](/static/images/modernizr/1/workflow-03.png)

Monitor your backend terminal for request logging, which demonstrates the API request flow.

### Frontend Application Access

Access the e-commerce frontend by navigating to `[your-url]/store/`:

![Store](/static/images/modernizr/1/workflow-04.png)

## System Interaction Analysis

Explore the application functionality to understand the data access patterns that will need to be modernized:

**User Registration:** Create a new user account to observe authentication workflows

**Admin Access:** Use the administrative account (username: `admin`, password: `0137183966133de0ace3d7e65e025d12`) to access extended functionality

**E-commerce Operations:** Navigate through product browsing, cart management, and checkout processes. We have two simulated payment methods, paypal and credit card, both will auto-approve any order!

Pay close attention to the backend terminal output as you interact with the application. Each user action generates specific database queries that represent the access patterns you'll need to replicate in your DynamoDB implementation.

## Baseline Understanding

This exploration phase establishes your baseline understanding of the current system architecture. Each user interaction demonstrates how the Express.js backend translates HTTP requests into MySQL queries, processes the results, and returns formatted responses to the React frontend.

This request-response cycle represents the core functionality that must be preserved during the database modernization process, ensuring zero functional regression while achieving improved performance and scalability through DynamoDB.
