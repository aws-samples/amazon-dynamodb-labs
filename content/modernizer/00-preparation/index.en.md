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

:image[Workshop Studio Tab]{src="/static/images/modernizer/0/LGAM-00-Step-01.png" disableZoom=true width=850}

Locate these two important values:
- **VSCodeServerPassword** - Authentication credential for your VS Code instance
- **VSCodeServerURLModernizer** - Direct endpoint to your cloud-based IDE

Your values are unique to you and will differ from the above example.

Click the `VSCodeServerURLModernizer` to launch your development environment. Enter the password when prompted and allow approximately 60 seconds for the environment to initialize. Any startup notifications can be safely dismissed.

## Step 2: Configuring the Cline AI Agent

Your workspace includes **Cline**, an autonomous AI coding agent that will assist with the modernization process. Cline provides intelligent code analysis, generation, and refactoring capabilities throughout this workshop.

Access the [Cline](https://cline.bot/) extension through the VS Code interface:

:image[Cline plugin]{src="/static/images/modernizer/0/LGAM-00-Step-02.png" disableZoom=true width=425}

## Step 3: Establishing Bedrock Integration

Configure Cline to use Amazon Bedrock as its foundation model provider. Select "Bring my own API Key",  choose "Amazon Bedrock" from the dropdown and select Continue:

:image[Cline API config 1]{src="/static/images/modernizer/0/LGAM-00-Step-03a.png" disableZoom=true width=425 height=700}
:image[Cline API config 2]{src="/static/images/modernizer/0/LGAM-00-Step-03b.png" disableZoom=true width=425 height=700}

Apply the following configuration parameters:
- **Authentication**: AWS Profile
- **Profile**: empty (default)
- **Region**: us-west-2
- **Cross region inference**: enabled

Confirm the settings and click on the Continue button:

:image[Cline API config 3]{src="/static/images/modernizer/0/LGAM-00-Step-03c.png" disableZoom=false width=425}

::alert[You are working in a lab environment, the foundational models have configured rate limiting, it is highly likely during the workshop you will get throttled and you will have to retry the operations. You have 4 request per minute using Claude 4 and 6 request per minute using Claude 3.7.]{type="info"}


## Step 4: Validating the Integration

Verify the Bedrock connection is functioning correctly by sending the below test prompt to Cline. If you are throttled, press "proceed anyway" to retry the request.

```terminal
Hello and Welcome to this modernization project, can you confirm you can read and list all the files in the workspace?
```

:image[Cline test]{src="/static/images/modernizer/0/LGAM-00-Step-04a.png" disableZoom=false width=425}

This workshop provides access to two foundation models: `claude-sonnet-4` (latest generation with enhanced reasoning capabilities) and `claude-sonnet-3.7` (previous generation with proven reliability).

:image[Cline test]{src="/static/images/modernizer/0/LGAM-00-Step-04b.png" disableZoom=false width=425}

## Step 5: Configuring Auto-Approval Settings

Optimize Cline's efficiency by enabling automatic permissions for routine operations. Access the auto-approve settings via the `^` icon in the bottom-right corner of the Cline interface.

Enable the following capabilities:
- **Read all files** - Full workspace file access
- **Use MCP servers** - Integration with specialized AI tools
- **Edit project files** - Code modification permissions

Ensure to enable the option **Edit project files** otherwise you will have to approve the creation of every file during the execution of the modernization project. 

:image[Cline plugin auto-approve settings]{src="/static/images/modernizer/0/LGAM-00-Step-05.png" disableZoom=false width=425}

## Step 6: Verifying MCP Server Status

Access the MCP server management interface (stacked server icon) to confirm all specialized AI tools are operational. You should observe 3 active servers with green status indicators, confirming proper connectivity.

:image[Cline MCP Servers]{src="/static/images/modernizer/0/LGAM-00-Step-06.png" disableZoom=false width=425}

## Step 7: MCP Integration Verification

You can ask `Cline` which MCP servers have configured and how they operate, to simplify this step let's just ask what MCP servers you have configured and see how it will read the configuration file for its parameters. 

::alert[You are working in a pre-configured lab environment, as part of the initialization process we have updated the credentials, networking and account information so you can use the MCP servers.]{type="info"}

```shell
What MCP servers you have configured?
```

:image[Cline MCP Servers]{src="/static/images/modernizer/0/LGAM-00-Step-07.png" disableZoom=false width=425}

## Environment Ready

Your development environment is now fully configured with AI-assisted tooling. The integration of VS Code Web, Cline, Bedrock foundation models, and specialized MCP servers provides a comprehensive platform for the database modernization workflow.

Proceed to the next module to begin the systematic analysis of your legacy application.
