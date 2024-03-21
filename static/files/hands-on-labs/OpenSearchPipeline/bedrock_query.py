import argparse
import json
import boto3
from opensearchpy import OpenSearch, RequestsHttpConnection, AWSV4SignerAuth

# Function definitions remain mostly unchanged from your Lambda function.
# Ensure to adjust the Elasticsearch/OpenSearch and Bedrock service configurations as necessary.

def product_recommend(input_text, language, region, opensearch_host, model_id):
    # 构建bedrock与 es客户端
    credentials = boto3.Session().get_credentials()
    auth = AWSV4SignerAuth(credentials, region, 'es')
    opensearch_host = opensearch_host.replace('https://', '')
    esClient = OpenSearch(
        hosts=[{'host': opensearch_host, 'port': 443}],
        http_auth=auth,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection,
        pool_maxsize=20
    )
    brt = boto3.client(service_name='bedrock-runtime', region_name=region)
    if language == 'en':
        index = 'product-details-index-en'
    else: 
        index = 'product-details-index-cn'
    query = {  
      "size": 5,
      "sort": [
        {
          "_score": {
            "order": "desc"
          }
        }
      ],
      "_source": {
        "includes": ["ProductName", "Category", "Description", "ProductID","Image"]
      },
      "query": {
        "neural": {
          "product_embedding": {
            "query_text": input_text,
            "model_id": model_id,
            "k": 10
          }
        }
      }
    }
    # 拼接 prompt
    es_response = esClient.search(
        body = query,
        index = index
    )
    try:
        es_res = es_response['hits']['hits'][0]
    except json.JSONDecodeError as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'no result in system'})
        }
    # llm 构建答案
    if language == 'en':
        llm_prompt = 'Human: You are currently a professional clothing store assistant. The customer has asked you the following question: ' + input_text + ',You must respond to the customer inquiry using the provided information. Feel free to ask the customer for additional details if needed.' + str(es_res) + ' Assistant:'
    else: 
        llm_prompt = 'Human: 你现在是一个导购客服，需要帮助客户推荐商品，根据商品的描述信息，给客户推荐具体的商品名称和编号. 客户的问题如下: ' + input_text + ',你必须基于以下商品信息进行推荐.适当的时候如果客户问题不清晰，可以反问一些关键信息.' + str(es_res) + ' Assistant:'
    
    llm_request_body = json.dumps({
        "prompt": llm_prompt,
        "max_tokens_to_sample": 4000,
        "temperature": 0.1,
        "top_p": 0.9,
    })
    
    modelId = 'anthropic.claude-v2:1'
    accept = 'application/json'
    contentType = 'application/json'
    
    response = brt.invoke_model(body=llm_request_body, modelId=modelId, accept=accept, contentType=contentType)
    
    response_body = json.loads(response.get('body').read())
    
    llm_result = response_body.get('completion')
    return llm_result,es_response

def reviews_analytis(input_text, language, region, opensearch_host, model_id):
    # 构建bedrock与 es客户端
    credentials = boto3.Session().get_credentials()
    auth = AWSV4SignerAuth(credentials, region, 'es')
    opensearch_host = opensearch_host.replace('https://', '')
    esClient = OpenSearch(
        hosts=[{'host': opensearch_host, 'port': 443}],
        http_auth=auth,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection,
        pool_maxsize=20
    )
    brt = boto3.client(service_name='bedrock-runtime', region_name=region)
    if language == 'en':
        index = 'product-reviews-index-en'
    else: 
        index = 'product-reviews-index-cn'
    query = {  
        "size" :50,
        "_source": {
          "includes": "combined_field"
        },
        "query": {
            "neural": {
              "product_reviews_embedding": {
                "query_text": input_text,
                "model_id": model_id,
                "k": 10
              }
            }
          }
    }
    es_response = esClient.search(
        body = query,
        index = index
    )
    try:
        es_res = es_response['hits']['hits'][0]
    except json.JSONDecodeError as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'no result in system'})
        }
    # llm 构建答案
    if language == 'en':
        llm_prompt = 'Human: You are now a customer service representative assisting customers in analyzing product reviews. Based on the historical comments about the product, you need to provide customers with a summary of the reviews, focusing primarily on the product rating and the emotional expressions conveyed in the comments. The customer\'s inquiries are as follows: ' + input_text + ',You must respond to the customer inquiry using the provided information. Feel free to ask the customer for additional details if needed.' + str(es_res) + ' Assistant:'
    else: 
        llm_prompt = 'Human: 你现在是一个导购客服，需要帮助客户分析商品的评价，根据商品过去的评论信息，给客户做评论总结，主要关注商品的评分，评论内容的情绪表达. 客户的问题如下: ' + input_text + ',你必须基于以下商品评价信息进行总结.适当的时候如果客户问题不清晰，可以反问一些关键信息.' + str(es_res) + ' Assistant:'
    
    llm_request_body = json.dumps({
        "prompt": llm_prompt,
        "max_tokens_to_sample": 4000,
        "temperature": 0.1,
        "top_p": 0.9,
    })
    
    modelId = 'anthropic.claude-v2:1'
    accept = 'application/json'
    contentType = 'application/json'
    
    response = brt.invoke_model(body=llm_request_body, modelId=modelId, accept=accept, contentType=contentType)
    
    response_body = json.loads(response.get('body').read())
    
    llm_result = response_body.get('completion')
    return llm_result,es_response


def main():
    parser = argparse.ArgumentParser(description='Product Recommendation and Review Analysis Script')
    parser.add_argument('type', choices=['product_recommend', 'reviews_analytis'], help='Type of operation to perform')
    parser.add_argument('language', choices=['en', 'cn'], help='Language version (en for English, cn for Chinese)')
    parser.add_argument('input_text', help='Input text for analysis or recommendation')
    parser.add_argument('region', help='AWS Region')
    parser.add_argument('opensearch_host', help='OpenSearch host URL')
    parser.add_argument('model_id', help='Model ID for neural search')
    
    args = parser.parse_args()

    if args.type == 'product_recommend':
        llm_result, es_response = product_recommend(args.input_text, args.language, args.region, args.opensearch_host, args.model_id)
    else:
        llm_result, es_response = reviews_analytis(args.input_text, args.language, args.region, args.opensearch_host, args.model_id)

    print(json.dumps({
        'llm_result': llm_result,
        'es_response': es_response
    }, indent=2))

if __name__ == '__main__':
    main()