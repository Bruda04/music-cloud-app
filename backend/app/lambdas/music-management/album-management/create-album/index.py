import base64
import json
import boto3
import uuid
from datetime import datetime

s3 = boto3.client('s3')
BUCKET = 'music-app-content-dhox6eq69e'

dynamodb = boto3.resource('dynamodb')
albums_table = dynamodb.Table('Albums')
genres_table = dynamodb.Table('Genres')

def lambda_handler(event, context):
    try:
        body = json.loads(event.get('body', '{}'))

        required_fields = ['title', 'artistIds', 'genres', 'tracks']
        missing = [f for f in required_fields if f not in body or not body[f]]
        if missing:
            return {
                'statusCode': 400,
                'headers': _cors_headers(),
                'body': json.dumps({'message': f'Missing required fields: {", ".join(missing)}'})
            }

        track_file_keys = []
        for track in body['tracks']:
            if 'file' not in track or not track['file']:
                return {
                    'statusCode': 400,
                    'headers': _cors_headers(),
                    'body': json.dumps({'message': f'Missing file for track {track.get("title", "")}'})
                }

            file_bytes = base64.b64decode(track['file'])
            timestamp = int(datetime.utcnow().timestamp())
            safe_title = track.get('title', 'track').replace(' ', '_')
            key = f"albums/{timestamp}-{safe_title}.mp3"

            s3.put_object(
                Bucket=BUCKET,
                Key=key,
                Body=file_bytes,
                ContentType='audio/mpeg'
            )

            track_file_keys.append({
                'title': track.get('title', ''),
                'fileKey': key
            })

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

        album_id = str(uuid.uuid4())
        item = {
            'albumId': album_id,
            'title': body['title'],
            'artistIds': body['artistIds'],
            'genres': genres,
            'tracks': track_file_keys,
            'createdAt': datetime.utcnow().isoformat()
        }

        if 'other' in body and isinstance(body['other'], dict):
            for k, v in body['other'].items():
                if k not in item:
                    item[k] = v
                else:
                    item[f'other_{k}'] = v

        albums_table.put_item(Item=item)

        return {
            'statusCode': 201,
            'headers': _cors_headers(),
            'body': json.dumps({
                'message': 'Album and tracks uploaded successfully',
                'albumId': album_id,
                'tracks': track_file_keys
            })
        }

    except Exception as e:
        print("Error:", e)
        return {
            'statusCode': 500,
            'headers': _cors_headers(),
            'body': json.dumps({'message': f'Failed to upload album: {str(e)}'})
        }

def _cors_headers():
    return {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "*",
        "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
        "Content-Type": "application/json"
    }