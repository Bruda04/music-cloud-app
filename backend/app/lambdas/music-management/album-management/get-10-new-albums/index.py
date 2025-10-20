import json
import os
import boto3
from decimal import Decimal

dynamodb = boto3.resource('dynamodb', region_name=os.environ["REGION"])
albums_table = dynamodb.Table(os.environ['ALBUMS_TABLE'])

def lambda_handler(event, context):
    try:
        response = albums_table.scan()
        items = response.get('Items', [])

        items_sorted = sorted(items, key=lambda x: x.get('createdAt', ''), reverse=True)
        latest_albums = items_sorted[:10]
        latest_albums = convert_decimals(latest_albums)

        return {
            'statusCode': 200,
            'headers': _cors_headers(),
            'body': json.dumps(latest_albums)
        }

    except Exception as e:
        print("Error:", e)
        return {
            'statusCode': 500,
            'headers': _cors_headers(),
            'body': json.dumps({'message': f'Failed to fetch albums: {str(e)}'})
        }

def convert_decimals(obj):
    if isinstance(obj, list):
        return [convert_decimals(i) for i in obj]
    elif isinstance(obj, dict):
        return {k: convert_decimals(v) for k, v in obj.items()}
    elif isinstance(obj, Decimal):
        return float(obj)
    else:
        return obj

def _cors_headers():
    return {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "*",
        "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
        "Content-Type": "application/json"
    }