import json
import boto3
import os
from boto3.dynamodb.types import TypeDeserializer

dynamodb = boto3.resource('dynamodb', region_name=os.environ["REGION"])
table = dynamodb.Table(os.environ["GENRES_TABLE"])

def lambda_handler(event, context):
    try:
        response = table.scan()
        items = response.get('Items', [])

        return {
            'statusCode': 200,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps(items)
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
