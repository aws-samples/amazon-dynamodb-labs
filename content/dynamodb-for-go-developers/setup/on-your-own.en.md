---
title: "Start: On your own"
date: 2019-12-02T07:05:12-08:00
weight: 20
chapter: true
---

::alert[Only complete this section if you are running the workshop on your own. If you are at an AWS hosted event (such as re\:Invent, Immersion Day, etc), go to :link[At an AWS hosted Event]{href="/dynamodb-for-go-developers/setup/aws-ws-event"}]

## Prerequisites

Before starting, ensure you have:

- **Go 1.21+** installed ([download here](https://go.dev/dl/))
- **Git** installed (to clone the workshop's lab branch)
- **AWS CLI** installed and configured with credentials ([install guide](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html))
- A terminal or IDE with Go support

Verify your setup:

```bash
go version
```

Expected output (version may vary):
```text
go version go1.21.0 darwin/arm64
```

Verify AWS credentials are configured:

```bash
aws sts get-caller-identity
```

You should see your account ID and ARN in the response. If you get an error, configure your credentials:

```bash
aws configure
```

::alert[During the course of this lab, you will create a DynamoDB table that incurs a small cost. Ensure you delete the table when you have completed the lab. The cleanup instructions are provided in the final module.]{type="warning"}

Once your environment is ready, continue on to: :link[Set up the Go project]{href="/dynamodb-for-go-developers/setup/step1"}.
