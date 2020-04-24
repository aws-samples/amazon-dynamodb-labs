+++
title = "Step 1 - Creating the GSI"
date = 2019-12-02T10:45:31-08:00
weight = 1
+++


The global secondary index for this exercise was created during the setup stage of this workshop. You can see the description of the global secondary index by executing the following AWS CLI command.
```bash
aws dynamodb describe-table --table-name logfile_scan --query "Table.GlobalSecondaryIndexes"
```
The description of the global secondary indexes should look like the following.
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

The DynamoDB `ItemCount` in this example is zero. DynamoDB calculates the total item count seen in this API many times throughout the day, and it may be possible that you see a different number than what the preceding output shows. This is normal.
