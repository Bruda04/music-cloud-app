import base64
import json
import os
import boto3
from datetime import datetime

from boto3.dynamodb.conditions import Key

s3 = boto3.client('s3')
BUCKET = os.environ['BUCKET']

dynamodb = boto3.resource('dynamodb', region_name=os.environ["REGION"])
songs_table = dynamodb.Table(os.environ['SONGS_TABLE'])
genres_table = dynamodb.Table(os.environ['GENRES_TABLE'])
songs_table_gsi_id = os.environ['SONGS_TABLE_GSI_ID']
artists_table = dynamodb.Table(os.environ['ARTISTS_TABLE'])
genre_content_table = dynamodb.Table(os.environ['GENRE_CONTENTS_TABLE'])

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

        artist = artists_table.get_item(Key={'artistId': body['artistId']}).get('Item')
        if not artist or (artist and artist.get('isDeleted', False)):
            return {
                'statusCode': 400,
                'headers': _cors_headers(),
                'body': json.dumps({'message': 'Artist does not exist or has been deleted.'})
            }
            
        required_fields = ['songId', 'title', 'artistId', 'genres', 'file', 'otherArtistIds']
        missing = [f for f in required_fields if f not in body or not body[f]]
        if missing:
            return {
                'statusCode': 400,
                'headers': _cors_headers(),
                'body': json.dumps({'message': f'Missing required fields: {", ".join(missing)}'})
            }

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

        song_keys = songs_table.query(
            IndexName=songs_table_gsi_id,
            KeyConditionExpression=Key("songId").eq(body['songId'])
        )

        if song_keys['Count'] == 0 or song_keys['Items'] is None:
            return {
                'statusCode': 404,
                'headers': _cors_headers(),
                'body': json.dumps({'message': 'Song not found'})
            }

        existing_song_resp = songs_table.get_item(Key={'songId': body['songId'], 'artistId': song_keys['Items'][0]['artistId']})
        existing_song = existing_song_resp.get('Item')

        key=body.get('file')
        if body.get('fileChanged', False):
            existing_song_resp = songs_table.get_item(Key={'songId': body['songId'], 'artistId': song_keys['Items'][0]['artistId']})
            if not existing_song:
                return {
                    'statusCode': 404,
                    'headers': _cors_headers(),
                    'body': json.dumps({'message': 'Song not found'})
                }
                
            file_bytes = base64.b64decode(body['file'])
            key = existing_song.get('fileKey', f"{int(datetime.utcnow().timestamp())}-{body['title'].replace(' ', '_')}.mp3")

            s3.put_object(
                Bucket=BUCKET,
                Key=f"songs/{key}",
                Body=file_bytes,
                ContentType='audio/mpeg'
            )
         
        item = existing_song.copy()
        genres_to_add = list(set(genres) - set(item.get('genres', [])))
        genres_to_remove = list(set(item.get('genres', [])) - set(genres))

        item.update({
            'songId': item.get('songId'),
            'title': body.get('title', existing_song.get('title')),
            'artistId': body.get('artistIds', existing_song.get('artistId', '')),
            'otherArtistIds': body.get('otherArtistIds', existing_song.get('otherArtistIds', [])),
            'genres': genres,
            'fileKey': key,
            'updatedAt': datetime.utcnow().isoformat()
        })

        
        if 'other' in body and isinstance(body['other'], dict):
            for k, v in body['other'].items():
                if k not in item:
                    item[k] = v
                else:
                    item[f'other_{k}'] = v

        songs_table.put_item(Item=item)

        for genre in genres_to_add:
            genre_content_table.put_item(
                Item={
                    'genreName': genre,
                    'contentKey': f"song#{item.get('songId')}"
                }
            )

        for genre in genres_to_remove:
            genre_content_table.delete_item(
                Key={
                    'genreName': genre,
                    'contentKey': f"song#{item.get('songId')}"
                }
            )

        return {
            'statusCode': 201,
            'headers': _cors_headers(),
            'body': json.dumps({
                'message': 'Song updated and metadata saved successfully',
                'songId': body['songId'],
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