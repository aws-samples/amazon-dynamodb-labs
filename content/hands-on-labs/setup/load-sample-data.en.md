+++
title = "Load Sample Data"
date = 2020-04-21T07:38:58-05:00
weight = 15
+++

Download and unzip the sample data:

    wget https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/samples/sampledata.zip

    unzip sampledata.zip

Load the sample data using the `batch-write-item` CLI:

    aws dynamodb batch-write-item --request-items file://ProductCatalog.json

    aws dynamodb batch-write-item --request-items file://Forum.json

    aws dynamodb batch-write-item --request-items file://Thread.json

    aws dynamodb batch-write-item --request-items file://Reply.json

After each data load you should get this message saying that there were no Unprocessed Items:

    {
        "UnprocessedItems": {}
    }

![Cloud9 Setup](/images/hands-on-labs/setup/load_data.png)
