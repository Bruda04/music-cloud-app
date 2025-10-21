import json
import os
from datetime import datetime
import boto3

dynamodb = boto3.resource('dynamodb', region_name=os.environ["REGION"])
listening_history_table = dynamodb.Table(os.environ["LISTENING_HISTORY_TABLE"])
artists_table = dynamodb.Table(os.environ["ARTISTS_TABLE"])

def lambda_handler(event, context):
    try:
        claims = event.get("requestContext", {}).get("authorizer", {}).get("claims", {})
        user = claims.get("email")

        if not user:
            return _response(400, {'error': 'User email not found in token'})

        body = json.loads(event.get('body', '{}'))
        content_type = body.get('contentType')
        content_id = body.get('contentId')
        artist_id = body.get('artistId')
        timestamp = datetime.utcnow().isoformat()

        if not content_type or not content_id or not artist_id:
            return _response(400, {'error': 'contentType, contentId, and artistId are required'})

        artist = artists_table.get_item(Key={'artistId': artist_id}).get('Item')
        if not artist or artist.get('isDeleted', False):
            artist_id = 'unknown-artist'

        listening_history_table.put_item(
            Item={
                'user': user,
                'timestamp': timestamp,
                'contentType': content_type,
                'contentId': content_id,
                'artistId': artist_id
            }
        )

        return _response(200, {'message': 'Listening history recorded successfully'})

    except Exception as e:
        return _response(500, {'error': str(e)})

def _response(status_code, body):
    return {
        'statusCode': status_code,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',
            'Content-Type': 'application/json'
        },
        'body': json.dumps(body)
    }
