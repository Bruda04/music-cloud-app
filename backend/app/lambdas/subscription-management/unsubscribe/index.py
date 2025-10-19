import json
import os
import boto3

dynamodb = boto3.resource('dynamodb', region_name=os.environ["REGION"])
subscriptions_table = dynamodb.Table(os.environ["SUBSCRIPTIONS_TABLE"])

def lambda_handler(event, context):
    try:
        claims = event.get("requestContext", {}).get("authorizer", {}).get("claims", {})
        user = claims.get("email")

        if not user:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'User email not found in token'})
            }

        body = json.loads(event.get('body', '{}'))
        content_type = body.get('contentType')
        content_id = body.get('contentId')
        if not content_type or not content_id:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'contentType and contentId are required'})
            }

        contentKey = f"{content_type}#{content_id}"

        subscriptions_table.delete_item(
            Key={
                'contentKey': contentKey,
                'user': user
            }
        )

        return {
            'statusCode': 200,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'message': 'Unsubscribed successfully'})
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
