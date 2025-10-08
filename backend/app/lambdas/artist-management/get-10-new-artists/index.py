import json
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
artists_table = dynamodb.Table('Artists')

def lambda_handler(event, context):
    try:
        response = artists_table.scan() 
        items = response.get('Items', [])
        
        items_sorted = sorted(items, key=lambda x: x.get('createdAt', ''), reverse=True)
        latest_artists = items_sorted[:10]
        
        return {
            'statusCode': 200,
            'headers': _cors_headers(),
            'body': json.dumps(latest_artists)
        }

    except Exception as e:
        print("Error:", e)
        return {
            'statusCode': 500,
            'headers': _cors_headers(),
            'body': json.dumps({'message': f'Failed to fetch artists: {str(e)}'})
        }

def _cors_headers():
    return {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "*",
        "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
        "Content-Type": "application/json"
    }
