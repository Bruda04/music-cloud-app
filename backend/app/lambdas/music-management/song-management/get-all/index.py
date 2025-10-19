import json
import os
from operator import index

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

        songs = []
        for song in items:
            core_fields = ['songId', 'title', 'artistId', 'genres', 'otherArtistsIds']
            mapped_song = {key: song.get(key, '' if key != 'otherArtistsIds' and key != 'genres' else []) for key in core_fields}
            mapped_song['file'] = song.get('fileKey')
            mapped_song['other'] = {k: v for k, v in song.items() if k not in core_fields and k != 'fileKey'}
            songs.append(mapped_song)

        result = {
            'songs': songs,
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
        return {
            'statusCode': 500,
            'body': json.dumps({'message': f'Failed to fetch songs: {str(e)}'})
        }
