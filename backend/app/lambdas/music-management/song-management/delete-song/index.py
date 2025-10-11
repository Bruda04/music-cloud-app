import json
import os
import boto3

s3 = boto3.client('s3')
BUCKET = os.environ['BUCKET']

dynamodb = boto3.resource('dynamodb', region_name=os.environ["REGION"])
songs_table = dynamodb.Table(os.environ['SONGS_TABLE'])

def lambda_handler(event, context):
    try:
        song_id = event.get('pathParameters', {}).get('id')
        if not song_id:
            return _response(400, 'Missing songId in path parameters')

        song_resp = songs_table.get_item(Key={'songId': song_id})
        song = song_resp.get('Item')
        if not song:
            return _response(404, 'Song not found')

        file_key = song.get('fileKey')
        if file_key:
            try:
                s3.delete_object(Bucket=BUCKET, Key=f"songs/{file_key}")
            except Exception as e:
                print(f"Warning: failed to delete S3 file {file_key}: {str(e)}")

        songs_table.delete_item(Key={'songId': song_id})

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
