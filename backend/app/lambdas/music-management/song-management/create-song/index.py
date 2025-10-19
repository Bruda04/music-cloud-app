import base64
import json
import os
import boto3
import uuid
from datetime import datetime

s3 = boto3.client('s3')
BUCKET = os.environ['BUCKET']

dynamodb = boto3.resource('dynamodb', region_name=os.environ["REGION"])
songs_table = dynamodb.Table(os.environ['SONGS_TABLE'])
genres_table = dynamodb.Table(os.environ['GENRES_TABLE'])
publishing_topic_arn = os.environ['SNS_PUBLISHING_CONTENT_TOPIC_ARN']
sns_client = boto3.client('sns', region_name=os.environ["REGION"])
artists_table = dynamodb.Table(os.environ['ARTISTS_TABLE'])
genre_contents_table = dynamodb.Table(os.environ['GENRE_CONTENTS_TABLE'])

def lambda_handler(event, context):
    try:
        claims = event.get("requestContext", {}).get("authorizer", {}).get("claims", {})
        if not claims.get("cognito:groups") or "Admins" not in claims.get("cognito:groups"):
            return {
                'statusCode': 403,
                'headers': _cors_headers(),
                'body': json.dumps({'message': 'Forbidden: Admins only'})
            }

        body = json.loads(event.get('body', '{}'))
        file_content_base64 = body.get('file')

        if not file_content_base64:
            return {
                'statusCode': 400,
                'headers': _cors_headers(),
                'body': json.dumps({'message': 'Missing file'})
            }

        required_fields = ['title', 'artistId', 'genres']
        missing = [f for f in required_fields if f not in body or not body[f]]
        if missing:
            return {
                'statusCode': 400,
                'headers': _cors_headers(),
                'body': json.dumps({'message': f'Missing required fields: {", ".join(missing)}'})
            }

        file_bytes = base64.b64decode(file_content_base64)
        timestamp = int(datetime.utcnow().timestamp())
        key = f"{timestamp}-{body['title'].replace(' ', '_')}.mp3"

        s3.put_object(
            Bucket=BUCKET,
            Key=f"songs/{key}",
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
            'artistId': body['artistId'],
            'otherArtistIds': body['otherArtistIds'] if 'otherArtistIds' in body else [],
            'genres': genres,
            'fileKey': key,
            'createdAt': datetime.utcnow().isoformat(),
            'imageFile': None,
            'lyrics': '',
            'ratingSum': 0,
            'ratingCount': 0,
        }

        if 'other' in body and isinstance(body['other'], dict):
            for k, v in body['other'].items():
                if k not in item:
                    item[k] = v
                else:
                    item[f'other_{k}'] = v

        songs_table.put_item(Item=item)

        artist = artists_table.get_item(Key={'artistId': body['artistId']}).get('Item')
        artist_name = artist['name'] if artist else 'Unknown Artist'

        publish_notification(
            artist_id=body['artistId'],
            genres=genres,
            artist_name= artist_name,
            song_title=body['title'],
            song_id=song_id
        )

        for genre in genres:
            genre_contents_table.put_item(
                Item={
                    'genre': genre,
                    'contentKey': f'song#{song_id}',
                }
            )

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

def publish_notification(artist_id, genres, artist_name, song_title, song_id):
    payload = {
        'artistId': artist_id,
        'songId': song_id,
        'genres': genres,
        'metadata': {
            'from': artist_name,
            'contentName': song_title,
            'contentType': 'song'
        }
    }
    sns_client.publish(
        TopicArn=publishing_topic_arn,
        Message=json.dumps(payload),
    )

def _cors_headers():
    """Utility for consistent CORS headers"""
    return {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "*",
        "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
        "Content-Type": "application/json"
    }
