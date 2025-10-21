import json
import os
from datetime import datetime

import boto3

dynamodb = boto3.resource('dynamodb', region_name=os.environ["REGION"])
listening_history_table = dynamodb.Table(os.environ["LISTENING_HISTORY_TABLE"])

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
        album_id = body.get('albumId')
        song_id = body.get('songId')
        artist_id = body.get('artistId')
        timestamp = datetime.utcnow().isoformat()
        content_id = f'{artist_id}#{album_id}#{song_id}' if content_type == 'album' else f'{artist_id}#{song_id}'

        if not content_type or not content_id or not artist_id:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'contentType, contentId, and artistId are required'})
            }

        listening_history_table.put_item(
            Item={
                'user': user,
                'timestamp': timestamp,
                'contentType': content_type,
                'contentId': content_id,
                'artistId': artist_id,
            }
        )

        return {
            'statusCode': 200,

            'body': json.dumps({'message': 'Notifications sent successfully'})
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }