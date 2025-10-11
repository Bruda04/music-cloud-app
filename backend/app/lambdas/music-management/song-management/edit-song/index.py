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

def lambda_handler(event, context):
    try:
        body = json.loads(event.get('body', '{}'))

        required_fields = ['songId', 'title', 'artistIds', 'genres', 'file']
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
        
        key=body.get('file')
        if body.get('fileChanged', False):
            existing_song_resp = songs_table.get_item(Key={'songId': body['songId']})
            existing_song = existing_song_resp.get('Item')
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
         
        item = {
            'songId': body['songId'],
            'title': body['title'],
            'artistIds': body['artistIds'],
            'genres': genres,
            'fileKey':key,
            'updatedAt': datetime.utcnow().isoformat()
        }
        
        if 'other' in body and isinstance(body['other'], dict):
            for k, v in body['other'].items():
                if k not in item:
                    item[k] = v
                else:
                    item[f'other_{k}'] = v

        songs_table.put_item(Item=item)

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