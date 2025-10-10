import json
import boto3

dynamodb = boto3.resource('dynamodb')
songs_table = dynamodb.Table('Songs')

def lambda_handler(event, context):
    try:
        song_id = event.get('pathParameters', {}).get('id')
        if not song_id:
            return {
                'statusCode': 400,
                'headers': _cors_headers(),
                'body': json.dumps({'message': 'Missing songId in path parameters'})
            }

        response = songs_table.get_item(Key={'songId': song_id})
        item = response.get('Item')
        if not item:
            return {
                'statusCode': 404,
                'headers': _cors_headers(),
                'body': json.dumps({'message': 'Song not found'})
            }

        core_fields = ['songId', 'title', 'artistIds', 'genres']
        mapped_song = {key: item.get(key, '' if key not in ['artistIds','genres'] else []) for key in core_fields}
        mapped_song['file'] = item.get('fileKey')
        mapped_song['other'] = {k: v for k, v in item.items() if k not in core_fields and k != 'fileKey'}

        return {
            'statusCode': 200,
            'headers': _cors_headers(),
            'body': json.dumps(mapped_song)
        }

    except Exception as e:
        print("Error:", e)
        return {
            'statusCode': 500,
            'headers': _cors_headers(),
            'body': json.dumps({'message': f'Failed to fetch song: {str(e)}'})
        }


def _cors_headers():
    return {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "*",
        "Access-Control-Allow-Methods": "OPTIONS,GET",
        "Content-Type": "application/json"
    }
