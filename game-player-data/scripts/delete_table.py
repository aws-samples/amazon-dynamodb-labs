import boto3

dynamodb = boto3.client('dynamodb')

try:
    dynamodb.delete_table(TableName='battle-royale')
    print("Table deleted successfully.")
except Exception as e:
    print("Could not delete table. Please try again in a moment. Error:")
    print(e)
