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
        body = json.loads(event.get('body', '{}'))

        required_fields = ['title', 'artistId', 'genres', 'tracks', 'details', 'imageFile']
        missing = [f for f in required_fields if f not in body or not body[f]]
        if missing:
            return {
                'statusCode': 400,
                'headers': _cors_headers(),
                'body': json.dumps({'message': f'Missing required fields: {", ".join(missing)}'})
            }


        #Image handling
        image_bytes = base64.b64decode(body['imageFile'])
        timestamp = int(datetime.utcnow().timestamp())
        safe_title = body['title'].replace(' ', '_')

        # Detect image type
        image_type = imghdr.what(None, h=image_bytes)
        if image_type not in ['jpeg', 'png']:
            return {
                'statusCode': 400,
                'headers': _cors_headers(),
                'body': json.dumps({'message': 'Only JPG and PNG images are supported.'})
            }

        # Use jpg instead of jpeg for filename
        ext = 'jpg' if image_type == 'jpeg' else 'png'
        image_key = f"{timestamp}-{safe_title}.{ext}"

        s3.put_object(
            Bucket=BUCKET,
            Key=f"images/albums/{image_key}",
            Body=image_bytes,
            ContentType=f'image/{ext}'
        )

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
            key = f"{timestamp}-{safe_title}.mp3"

            s3.put_object(
                Bucket=BUCKET,
                Key=f"albums/{key}",
                Body=file_bytes,
                ContentType='audio/mpeg'
            )

            track_file_keys.append({
                'songId': str(uuid.uuid4()),
                'title': track.get('title', ''),
                'fileKey': key,
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

        publish_notification(body['artistId'], genres, artist_name, body['title'])

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

def publish_notification(artist_id, genres, artist_name, album_title):
    payload = {
        'artistId': artist_id,
        'genres': genres,
        'metadata': {
            'from': artist_name,
            'contentName': album_title,
            'contentType': 'album'
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