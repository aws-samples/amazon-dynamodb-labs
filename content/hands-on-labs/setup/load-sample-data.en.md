---
title: "Load Sample Data"
date: 2020-04-21T07:38:58-05:00
weight: 15
---

Download and unzip the sample data:

```bash
cd LHOL

curl -O https://amazon-dynamodb-labs.com/static/hands-on-labs/sampledata.zip

unzip sampledata.zip
```

Load the sample data using the `batch-write-item` CLI:

```bash
aws dynamodb batch-write-item --request-items file://ProductCatalog.json
```

```bash
aws dynamodb batch-write-item --request-items file://Forum.json
```

```bash
aws dynamodb batch-write-item --request-items file://Thread.json
```

```bash
aws dynamodb batch-write-item --request-items file://Reply.json
```

After each data load you should get this message saying that there were no Unprocessed Items:

```json
    {
        "UnprocessedItems": {}
    }
```

#### Sample output
![Processed Items](/static/images/hands-on-labs/load-sample-data.png)

You can now continue with the section :link[Explore DynamoDB with the CLI]{href="/hands-on-labs/explore-cli"}.  