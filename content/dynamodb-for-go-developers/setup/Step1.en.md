---
title: "Set up the Go project"
date: 2021-04-21T07:33:04-05:00
weight: 30
---

In this step, you install Go and clone the workshop's **lab branch** - a ready-to-run project where the DynamoDB operations are left as guided fill-in-the-blank exercises for you to complete.

## Install Go

Download and install Go 1.26.3 (or the latest version from [go.dev/dl](https://go.dev/dl/)):

```bash
rm -rf /usr/local/go && tar -C /usr/local -xzf go1.26.3.linux-amd64.tar.gz
```

You may need to run the command with `sudo`. Do not extract the archive into an existing `/usr/local/go` tree - this is known to produce broken Go installations.

Add `/usr/local/go/bin` to your `PATH` by appending the following line to `$HOME/.profile` (or `/etc/profile` for a system-wide installation):

```bash
export PATH=$PATH:/usr/local/go/bin
```

Apply the change immediately:

```bash
source $HOME/.profile
```

Verify the installation:

```bash
go version
```

Expected output (version may vary):
```text
go version go1.26.3 linux/amd64
```

::alert[If you are running on macOS or Windows, download the appropriate installer from [go.dev/dl](https://go.dev/dl/) and follow the platform-specific instructions.]{type="info"}

## Clone the lab branch

Clone the workshop repository and check out the **`lab`** branch. This branch contains the complete project scaffolding - data models, the CLI entry point, the CloudFormation template, and a demo harness - with the DynamoDB data-plane operations left as `TODO(lab)` stubs for you to fill in:

```bash
git clone -b lab https://github.com/aws-samples/sample-dynamodb-for-go-developers.git
cd sample-dynamodb-for-go-developers
```

Download the Go module dependencies:

```bash
go mod download
```

## Implementing Stubs

You implement the workshop one function at a time, directly in `repository.go`. 

1. **Read the concept** in the module page.
2. **Open `repository.go`** and find the function named in the instructions. Each one to implement carries a `// TODO(lab):` comment describing exactly what to do and which already-implemented function to mirror.
3. **Replace the stub body** with your implementation and delete its `return errNotImplemented(...)` line.
4. **Run the demo** (`go run . demo`) to check your work. Until a function is implemented it returns a `TODO(lab): ... not implemented` error, so the demo doubles as a live progress checklist - each function you complete lets it run one step further.

::alert[A few functions are already implemented as **worked examples** - one per core concept (for example `CreateUser`, `GetUser`, and `GetOrdersByUserID`). Read these first; the stubs for the same concept follow their shape.]{type="info"}

The full solution is on the **`main`** branch of the repository you just cloned. If you'd rather read through the completed implementation than fill in the stubs yourself, switch to that branch from the terminal:

```bash
git checkout main
```

This gives you the whole solution to review. To go back to the lab branch and implement the functions yourself, run `git checkout lab`.

## Explore the project

Take a moment to look at the files you cloned:

```text
.
├── template.yaml    # CloudFormation: table + GSIs + LSI (you deploy this in Module 2)
├── models.go        # Entity structs (User, Order, OrderItem) — provided
├── repository.go    # DynamoDB operations — worked examples + TODO(lab) stubs (you fill these in)
├── demo.go          # Sample dataset and the demo walkthrough — provided
├── main.go          # CLI entry point: config, client, subcommand dispatch — provided
├── go.mod
└── go.sum
```

Open `models.go` and read the three entity structs. Notice the `dynamodbav` struct tags - these control how the AWS SDK marshals and unmarshals Go structs to and from DynamoDB attribute values. The `User.Username` field uses `dynamodbav:"-"` because it is encoded in the partition key rather than stored as a separate attribute.

You do not run the project yet - it needs a table first. In the next module, you learn the data model and provision that table with CloudFormation.
