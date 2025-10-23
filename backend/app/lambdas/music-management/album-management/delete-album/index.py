import json
import os
import boto3
from boto3.dynamodb.conditions import Key

s3 = boto3.client('s3')
BUCKET = os.environ['BUCKET']

dynamodb = boto3.resource('dynamodb', region_name=os.environ["REGION"])
genre_contents_table = dynamodb.Table(os.environ['GENRE_CONTENTS_TABLE'])
albums_table = dynamodb.Table(os.environ['ALBUMS_TABLE'])
albums_table_gsi_id = os.environ['ALBUMS_TABLE_GSI_ID']

def lambda_handler(event, context):
    try:
        claims = event.get("requestContext", {}).get("authorizer", {}).get("claims", {})
        if not claims.get("cognito:groups") or "Admins" not in claims.get("cognito:groups"):
            return _response(403, 'Forbidden: Admins only')

        album_id = event.get('pathParameters', {}).get('id')
        if not album_id:
            return _response(400, 'Missing albumId in path parameters')

        keys = albums_table.query(
            IndexName=albums_table_gsi_id,
            KeyConditionExpression=Key("albumId").eq(album_id),
            ProjectionExpression="artistId"  # izvući samo što ti treba
        ).get("Items", [])

        if not keys:
            return _response(404, 'Song not found')
        album_keys = keys[0]

        albums_resp = albums_table.get_item(Key={'albumId': album_id, 'artistId': album_keys['artistId']})
        song = albums_resp.get('Item')
        if not song:
            return _response(404, 'Song not found')

        for track in song.get('tracks', []):
            file_key = track.get('fileKey')
            if file_key:
                try:
                    s3.delete_object(Bucket=BUCKET, Key=f"albums/{file_key}")
                except Exception as e:
                    pass

        albums_table.delete_item(Key={'albumId': album_id, 'artistId': album_keys['artistId']})

        genres = song.get('genres', [])
        for genre in genres:
            genre_contents_table.delete_item(
                Key={
                    'genreName': genre,
                    'contentKey': f"album#{album_keys['artistId']}#{album_id}"
                }
            )

        return _response(200, f'Song {album_id} deleted successfully')

    except Exception as e:
        return _response(500, f'Failed to delete song: {str(e)}')


def _response(status_code, message):
    return {
        'statusCode': status_code,
        'headers': {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "*",
            "Content-Type": "application/json"
        },
        'body': json.dumps({'message': message})
    }
