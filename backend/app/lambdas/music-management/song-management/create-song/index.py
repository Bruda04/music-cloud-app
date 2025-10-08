import base64
import json
import boto3
import uuid
from datetime import datetime

s3 = boto3.client('s3')
BUCKET = 'music-app-content-dhox6eq69e'

dynamodb = boto3.resource('dynamodb')
songs_table = dynamodb.Table('Songs')
genres_table = dynamodb.Table('Genres')


def lambda_handler(event, context):
    try:
        body = json.loads(event.get('body', '{}'))
        file_content_base64 = body.get('fileContentBase64')

        if not file_content_base64:
            return {
                'statusCode': 400,
                'headers': _cors_headers(),
                'body': json.dumps({'message': 'Missing fileContentBase64'})
            }

        required_fields = ['title', 'artistIds', 'genres']
        missing = [f for f in required_fields if f not in body or not body[f]]
        if missing:
            return {
                'statusCode': 400,
                'headers': _cors_headers(),
                'body': json.dumps({'message': f'Missing required fields: {", ".join(missing)}'})
            }

        file_bytes = base64.b64decode(file_content_base64)
        timestamp = int(datetime.utcnow().timestamp())
        key = f"songs/{timestamp}-{body['title'].replace(' ', '_')}.mp3"

        s3.put_object(
            Bucket=BUCKET,
            Key=key,
            Body=file_bytes,
            ContentType='audio/mpeg'
        )

        genres = [g.strip().lower() for g in body['genres'] if g.strip()]
        for genre in genres:
            try:
                genres_table.put_item(
                    Item={'genreName': genre},
                    ConditionExpression='attribute_not_exists(#g)',
                    ExpressionAttributeNames={'#g': 'genreName'}
                )
            except genres_table.meta.client.exceptions.ConditionalCheckFailedException:
                pass

        song_id = str(uuid.uuid4())
        item = {
            'songId': song_id,
            'title': body['title'],
            'artistIds': body['artistIds'],
            'genres': genres,
            'fileKey': key,
            'createdAt': datetime.utcnow().isoformat()
        }

        if 'other' in body:
            item['other'] = body['other']

        songs_table.put_item(Item=item)

        return {
            'statusCode': 201,
            'headers': _cors_headers(),
            'body': json.dumps({
                'message': 'Song uploaded and metadata saved successfully',
                'songId': song_id,
                'fileKey': key
            })
        }

    except Exception as e:
        print("Error:", e)
        return {
            'statusCode': 500,
            'headers': _cors_headers(),
            'body': json.dumps({'message': f'Failed to upload a song: {str(e)}'})
        }


def _cors_headers():
    """Utility for consistent CORS headers"""
    return {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "*",
        "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
        "Content-Type": "application/json"
    }
