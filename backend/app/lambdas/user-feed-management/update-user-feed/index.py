import json
import os
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb', region_name=os.environ["REGION"])
user_feed_table = dynamodb.Table(os.environ["USER_FEED_TABLE"])
subscriptions_table = dynamodb.Table(os.environ["SUBSCRIPTIONS_TABLE"])
subscriptions_table_gsi_id = os.environ["SUBSCRIPTIONS_TABLE_GSI_ID"]


def lambda_handler(event, context):
    try:
        claims = event.get("requestContext", {}).get("authorizer", {}).get("claims", {})
        user = claims.get("email")

        if not user:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'User email not found in token'})
            }


        return {
            'statusCode': 200,
            'body': json.dumps({'message': f'User feed update done for {user}'})
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
