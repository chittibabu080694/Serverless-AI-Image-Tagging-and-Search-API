import boto3
import os

s3 = boto3.client('s3')
rekognition = boto3.client('rekognition')
dynamodb = boto3.resource('dynamodb')

TABLE_NAME = os.environ.get('TABLE_NAME', 'ImageMetadata')
table = dynamodb.Table(TABLE_NAME)

def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    # Call Amazon Rekognition DetectLabels
    response = rekognition.detect_labels(
        Image={'S3Object': {'Bucket': bucket, 'Name': key}},
        MaxLabels=10,
        MinConfidence=75
    )

    tags = [label['Name'] for label in response['Labels']]

    # Save metadata to DynamoDB
    table.put_item(
        Item={
            'ImageKey': key,
            'Bucket': bucket,
            'Tags': tags
        }
    )

    return {'statusCode': 200, 'body': f"Successfully tagged {key} with {tags}"}
