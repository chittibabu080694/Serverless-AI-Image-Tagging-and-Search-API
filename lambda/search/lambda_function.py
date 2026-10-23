import boto3
import json
import os
from boto3.dynamodb.conditions import Attr

dynamodb = boto3.resource('dynamodb')
TABLE_NAME = os.environ.get('TABLE_NAME', 'ImageMetadata')
table = dynamodb.Table(TABLE_NAME)

def lambda_handler(event, context):
    query_params = event.get('queryStringParameters') or {}
    search_tag = query_params.get('tag', '').lower()

    if not search_tag:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Please provide a search tag using ?tag=keyword'})
        }

    # Scan DynamoDB for matching tags (for small-scale projects; use OpenSearch for production)
    response = table.scan(
        FilterExpression=Attr('Tags').contains(search_tag)
    )

    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps(response.get('Items', []))
    }
