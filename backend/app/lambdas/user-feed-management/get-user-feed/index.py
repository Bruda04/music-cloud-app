import json
import os

import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb', region_name=os.environ["REGION"])
user_feed_table = dynamodb.Table(os.environ["USER_FEED_TABLE"])

def lambda_handler(event, context):
    try:
        claims = event.get("requestContext", {}).get("authorizer", {}).get("claims", {})
        user = claims.get("email")

        if not user:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'User email not found in token'})
            }

        user_feed_table_resp = user_feed_table.query(
            KeyConditionExpression=Key('user').eq(user)
        )
        feed_items = user_feed_table_resp.get('Items', [])

        return {
            'statusCode': 200,
            'body': json.dumps({'feed': feed_items})
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
