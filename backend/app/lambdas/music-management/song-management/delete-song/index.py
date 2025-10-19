import json
import os
import boto3
from boto3.dynamodb.conditions import Key

s3 = boto3.client('s3')
BUCKET = os.environ['BUCKET']

dynamodb = boto3.resource('dynamodb', region_name=os.environ["REGION"])
songs_table = dynamodb.Table(os.environ['SONGS_TABLE'])
songs_table_gsi_id = os.environ['SONGS_TABLE_GSI_ID']
genre_contents_table = dynamodb.Table(os.environ['GENRE_CONTENTS_TABLE'])

def lambda_handler(event, context):
    try:
        claims = event.get("requestContext", {}).get("authorizer", {}).get("claims", {})
        if not claims.get("cognito:groups") or "Admins" not in claims.get("cognito:groups"):
            return _response(403, 'Forbidden: Admins only')

        song_id = event.get('pathParameters', {}).get('id')
        if not song_id:
            return _response(400, 'Missing songId in path parameters')

        keys = songs_table.query(
            IndexName=songs_table_gsi_id,
            KeyConditionExpression=Key("songId").eq(song_id),
            ProjectionExpression="artistId, albumId"  # izvući samo što ti treba
        ).get("Items", [])

        if not keys:
            return _response(404, 'Song not found')
        song_keys = keys[0]

        song_resp = songs_table.get_item(Key={'songId': song_id, 'artistId': song_keys['artistId']})
        song = song_resp.get('Item')
        if not song:
            return _response(404, 'Song not found')

        file_key = song.get('fileKey')
        if file_key:
            try:
                s3.delete_object(Bucket=BUCKET, Key=f"songs/{file_key}")
            except Exception as e:
                pass

        songs_table.delete_item(Key={'songId': song_id, 'artistId': song_keys['artistId']})

        genres = song.get('genres', [])
        for genre in genres:
            genre_contents_table.delete_item(
                Key={
                    'genreName': genre,
                    'contentKey': f"song#{song_id}"
                }
            )

        return _response(200, f'Song {song_id} deleted successfully')

    except Exception as e:
        return _response(500, f'Failed to delete song: {str(e)}')


def _response(status_code, message):
    return {
        'statusCode': status_code,
        'headers': {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Methods": "OPTIONS,DELETE,GET,POST",
            "Content-Type": "application/json"
        },
        'body': json.dumps({'message': message})
    }
