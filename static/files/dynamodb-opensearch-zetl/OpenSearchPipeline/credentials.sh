aws cloudformation describe-stacks --stack-name dynamodb-opensearch-setup --query "Stacks[0].Outputs" --output table > CloudFormation-Outputs.txt
export OPENSEARCH_ENDPOINT=`aws cloudformation describe-stacks --stack-name dynamodb-opensearch-setup --query "Stacks[0].Outputs[?OutputKey=='OSDomainEndpoint'].OutputValue" --output text`
TOKEN=$(curl -s -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600")
INSTANCE_ROLE=$(curl -s -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/iam/security-credentials/)
RESULTS=$(curl -s -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/iam/security-credentials/${INSTANCE_ROLE})

AccessKeyId=$(echo $RESULTS | jq -r '.AccessKeyId')
SecretAccessKey=$(echo $RESULTS | jq -r '.SecretAccessKey')
Region=$(curl -s -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/placement/availability-zone | sed 's/\(.*\)[a-z]/\1/')
Token=$(echo $RESULTS | jq -r '.Token')
Role=$(aws sts get-caller-identity | jq -r '.Arn | sub("sts";"iam") | sub("assumed-role";"role") | sub("/i-[a-zA-Z0-9]+$";"")')

export METADATA_AWS_ACCESS_KEY_ID=${AccessKeyId}
export METADATA_AWS_SECRET_ACCESS_KEY=${SecretAccessKey}
export METADATA_AWS_SESSION_TOKEN=${Token}
export METADATA_AWS_REGION=${Region}
export METADATA_AWS_ROLE=${Role}

echo "METADATA_AWS_ACCESS_KEY_ID: $AccessKeyId"
echo "METADATA_AWS_SECRET_ACCESS_KEY: $SecretAccessKey"
echo "METADATA_AWS_SESSION_TOKEN: $Token"
echo "METADATA_AWS_REGION: $Region"
echo "METADATA_AWS_ROLE: $Role"
echo "OPENSEARCH_ENDPOINT: $OPENSEARCH_ENDPOINT"