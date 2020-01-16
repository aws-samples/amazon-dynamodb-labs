+++
title = "Step 1 - Creating the GSI"
date = 2019-12-02T10:45:31-08:00
weight = 1
+++


The GSI for this exercise was created during the Setup phase for this workshop. You can see the description of the GSI via executing the following command:
```bash
aws dynamodb describe-table --table-name logfile_scan --query "Table.GlobalSecondaryIndexes"
```
You will see the description of the Global Secondary Indexes, which will look like the below:
```json
{
  "GlobalSecondaryIndexes": [
    {
        "IndexName": "GSI_1",
        "KeySchema": [
            {
                "AttributeName": "GSI_1_PK",
                "KeyType": "HASH"
            },
            {
                "AttributeName": "GSI_1_SK",
                "KeyType": "RANGE"
            }
        ],
        "Projection": {
            "ProjectionType": "KEYS_ONLY"
        },
        "IndexStatus": "ACTIVE",
        "ProvisionedThroughput": {
            "NumberOfDecreasesToday": 0,
            "ReadCapacityUnits": 3000,
            "WriteCapacityUnits": 5000
        },
        "IndexSizeBytes": 0,
        "ItemCount": 0,
        "IndexArn": "arn:aws:dynamodb:(region):(accountid):table/logfile_scan/index/GSI_1"
    }
]
}
```

The DynamoDB *ItemCount* is zero. DynamoDB calculates the total item count seen in this API many times throughout the day, and it may be possible that you see a different number than what the output shows. This is normal.
