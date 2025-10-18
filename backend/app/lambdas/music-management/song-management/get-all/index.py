import json
import os
import boto3

dynamodb = boto3.resource('dynamodb', region_name=os.environ["REGION"])
songs_table = dynamodb.Table(os.environ['SONGS_TABLE'])

def lambda_handler(event, context):
    try:
        limit = int(event.get('queryStringParameters', {}).get('limit', 10))
        last_key = event.get('queryStringParameters', {}).get('lastKey', None)

        scan_kwargs = {'Limit': limit}
        if last_key:
            scan_kwargs['ExclusiveStartKey'] = json.loads(last_key)

        response = songs_table.scan(**scan_kwargs)
        items = response.get('Items', [])

        songs_map = {}
        for song in items:
            song_id = song['songId']
            if song_id not in songs_map:
                songs_map[song_id] = {
                    'songId': song_id,
                    'title': song.get('title', None),
                    'genres': song.get('genres', []),
                    'file': song.get('fileKey', None),
                    'artistIds': [song['artistId']] if 'artistId' in song else []
                }
            else:
                if 'artistId' in song and song['artistId'] not in songs_map[song_id]['artistIds']:
                    songs_map[song_id]['artistIds'].append(song['artistId'])

                main_fields = ['title', 'genres', 'fileKey']
                for field in main_fields:
                    if songs_map[song_id].get(field) is None and field in song:
                        if field == 'fileKey':
                            songs_map[song_id]['file'] = song[field]
                        else:
                            songs_map[song_id][field] = song[field]

        result = {
            'songs': songs_map.values(),
            'lastKey': json.dumps(response.get('LastEvaluatedKey')) if 'LastEvaluatedKey' in response else None
        }

        return {
            'statusCode': 200,
            'headers': {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "OPTIONS,GET",
                "Content-Type": "application/json"
            },
            'body': json.dumps(result)
        }

    except Exception as e:
        print("Error:", e)
        return {
            'statusCode': 500,
            'body': json.dumps({'message': f'Failed to fetch songs: {str(e)}'})
        }
