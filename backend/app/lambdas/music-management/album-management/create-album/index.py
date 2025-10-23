import base64
import json
import boto3
import uuid
import os
from datetime import datetime
import imghdr


s3 = boto3.client('s3')
BUCKET = os.environ['BUCKET']

dynamodb = boto3.resource('dynamodb', region_name=os.environ["REGION"])
albums_table = dynamodb.Table(os.environ['ALBUMS_TABLE'])
genres_table = dynamodb.Table(os.environ['GENRES_TABLE'])
genre_contents_table = dynamodb.Table(os.environ['GENRE_CONTENTS_TABLE'])
artists_table = dynamodb.Table(os.environ['ARTISTS_TABLE'])

publishing_topic_arn = os.environ['SNS_PUBLISHING_CONTENT_TOPIC_ARN']
sns_client = boto3.client('sns', region_name=os.environ["REGION"])

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

        required_fields = ['title', 'artistId', 'genres', 'tracks', 'details']
        missing = [f for f in required_fields if f not in body or not body[f]]
        if missing:
            return {
                'statusCode': 400,
                'headers': _cors_headers(),
                'body': json.dumps({'message': f'Missing required fields: {", ".join(missing)}'})
            }

        artist = artists_table.get_item(Key={'artistId': body['artistId']}).get('Item')
        if not artist or (artist and artist.get('isDeleted', False)):
            return {
                'statusCode': 400,
                'headers': _cors_headers(),
                'body': json.dumps({'message': 'Artist does not exist or has been deleted.'})
            }

        #Image handling
        timestamp = int(datetime.utcnow().timestamp())
        safe_title = body['title'].replace(' ', '_')
        # Use jpg instead of jpeg for filename
        image_key = f"{timestamp}-{safe_title}.png"

        image_upload_url = s3.generate_presigned_url(
            'put_object',
            Params={'Bucket': BUCKET, 'Key': f'images/albums/{image_key}', 'ContentType': 'image/png'},
            ExpiresIn=3600
        )


        track_file_keys = []
        track_upload_urls = []
        for track in body['tracks']:
            timestamp = int(datetime.utcnow().timestamp())
            safe_title = track.get('title', 'track').replace(' ', '_')
            track_key = f"{timestamp}-{safe_title}.mp3"

            song_upload_url = s3.generate_presigned_url(
                'put_object',
                Params={'Bucket': BUCKET, 'Key': f'albums/{track_key}', 'ContentType': 'audio/mpeg'},
                ExpiresIn=3600
            )
            track_upload_urls.append(song_upload_url)

            track_file_keys.append({
                'songId': str(uuid.uuid4()),
                'title': track.get('title', ''),
                'fileKey': track_key,
                'artistId': body['artistId'],
                'otherArtistIds': track.get('otherArtistIds', []),
                'lyrics': '',
                'ratingSum': 0,
                'ratingCount': 0,
                'genres': body['genres']
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
            'artistId': body['artistId'],
            'genres': genres,
            'tracks': track_file_keys,
            'createdAt': datetime.utcnow().isoformat(),
            'details': body['details'],
            'imageFile': image_key
        }

        if 'other' in body and isinstance(body['other'], dict):
            for k, v in body['other'].items():
                if k not in item:
                    item[k] = v
                else:
                    item[f'other_{k}'] = v

        albums_table.put_item(Item=item)

        for genre in genres:
            genre_contents_table.put_item(
                Item={
                    'genreName': genre,
                    'contentKey': f'album#{body['artistId']}#{album_id}',
                }
            )


        artist = artists_table.get_item(Key={'artistId': body['artistId']}).get('Item')
        artist_name = artist['name'] if artist else 'Unknown Artist'

        publish_notification(body['artistId'], genres, artist_name, body['title'], album_id)

        return {
            'statusCode': 201,
            'headers': _cors_headers(),
            'body': json.dumps({
                'message': 'Album and tracks uploaded successfully',
                'albumId': album_id,
                'tracks': track_file_keys,
                'trackUploadUrls': track_upload_urls,
                'imageUploadUrl': image_upload_url,
            })
        }

    except Exception as e:
        print("Error:", e)
        return {
            'statusCode': 500,
            'headers': _cors_headers(),
            'body': json.dumps({'message': f'Failed to upload album: {str(e)}'})
        }

def publish_notification(artist_id, genres, artist_name, album_title, album_id):
    payload = {
        'artistId': artist_id,
        'genres': genres,
        'albumId': album_id,
        'metadata': {
            'from': artist_name,
            'contentName': album_title,
            'contentType': 'album',
        }
    }
    sns_client.publish(
        TopicArn=publishing_topic_arn,
        Message=json.dumps(payload),
    )


def _cors_headers():
    return {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "*",
        "Content-Type": "application/json"
    }