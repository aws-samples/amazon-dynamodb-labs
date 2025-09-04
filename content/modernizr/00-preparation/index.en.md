---
title: "Environment Setup"
date: 2025-09-01T09:53:04-05:00
weight: 30
chapter: true
---

## Development Environment Setup

Before beginning the modernization process, you need to configure your development environment. You'll be working with Visual Studio Code Web running on a pre-configured EC2 instance that includes all necessary AWS permissions and tooling for this workshop. This cloud-based development environment provides immediate access to AWS services and the specialized MCP servers required for the modernization workflow, eliminating the need for local environment configuration.

## Step 1: Accessing Your Development Environment

Navigate to the workshop studio page and access the "Outputs" tab to retrieve your environment credentials:

![Workshop studio tab](/static/images/modernizr/0/setup-01.png)

Locate these two important values:
- **VSCodeServerPassword** - Authentication credential for your VS Code instance
- **VSCodeServerURL** - Direct endpoint to your cloud-based IDE

Click the `VSCodeServerURL` to launch your development environment. Enter the password when prompted and allow approximately 60 seconds for the environment to initialize. Any startup notifications can be safely dismissed.

## Step 2: Configuring the Cline AI Agent

Your workspace includes **Cline**, an autonomous AI coding agent that will assist with the modernization process. Cline provides intelligent code analysis, generation, and refactoring capabilities throughout this workshop.

Access the [Cline](https://cline.bot/) extension through the VS Code interface:

![Cline plugin](/static/images/modernizr/0/setup-02.png)

## Step 3: Establishing Bedrock Integration

Configure Cline to use Amazon Bedrock as its foundation model provider. Select "Use your own API Key" and choose "Amazon Bedrock" from the dropdown:

![Cline plugin API config](/static/images/modernizr/0/setup-03.png)

Apply the following configuration parameters:
- **Profile**: default 
- **Region**: us-west-2
- **Cross region inference**: enabled

Confirm the settings and initialize the connection:

![Cline plugin config](/static/images/modernizr/0/setup-04.png)


::alert[You are working in a lab environment, the foundational models have configured rate limiting, it is highly likely during the workshop you will get throttled and you will have to retry the operations. You have 4 request per minute using Claude 4 and 6 request per minute using Claude 3.7.]{type="info"}


## Step 4: Validating the Integration

Verify the Bedrock connection is functioning correctly by sending this test prompt to Cline:

```terminal
Hello and Welcome to this modernization project, can you confirm you can read and list all the files in the workspace?
```

![Cline plugin testing](/static/images/modernizr/0/setup-05.png)

This workshop provides access to two foundation models: `claude-sonnet-4` (latest generation with enhanced reasoning capabilities) and `claude-sonnet-3.7` (previous generation with proven reliability).

![Cline plugin response](/static/images/modernizr/0/setup-06.png) ![Cline plugin result](/static/images/modernizr/0/setup-07.png)

## Step 5: Configuring Auto-Approval Settings

Optimize Cline's efficiency by enabling automatic permissions for routine operations. Access the auto-approve settings via the `^` icon in the bottom-right corner of the Cline interface.

Enable the following capabilities:
- **Read all files** - Full workspace file access
- **Use MCP servers** - Integration with specialized AI tools
- **Edit project files** - Code modification permissions

Increase the **Max requests** parameter from 20 to 40 to accommodate complex multi-step operations without interruption.

![Cline plugin auto-approve settings](/static/images/modernizr/0/setup-08.png)

## Step 6: Verifying MCP Server Status

Access the MCP server management interface (stacked server icon) to confirm all specialized AI tools are operational. You should observe 3 active servers with green status indicators, confirming proper connectivity.

![Cline plugin auto-approve settings](/static/images/modernizr/0/setup-09.png)

## Step 7: MCP Integration Verification

Test the MCP server functionality by querying existing DynamoDB resources:

```shell
Please show me the DynamoDB tables that I have in this region
```

![Task MCP Server](/static/images/modernizr/0/setup-10.png)

## Environment Ready

Your development environment is now fully configured with AI-assisted tooling. The integration of VS Code Web, Cline, Bedrock foundation models, and specialized MCP servers provides a comprehensive platform for the database modernization workflow.

Proceed to the next module to begin the systematic analysis of your legacy application.
