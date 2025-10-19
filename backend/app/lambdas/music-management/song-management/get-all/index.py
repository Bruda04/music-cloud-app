import json
import os

import boto3

dynamodb = boto3.resource('dynamodb', region_name=os.environ["REGION"])
songs_table = dynamodb.Table(os.environ['SONGS_TABLE'])
artists_table = dynamodb.Table(os.environ['ARTISTS_TABLE'])

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
            core_fields = ['songId', 'title', 'genres']
            mapped_song = {key: song.get(key, '' if key != 'genres' else []) for key in core_fields}
            mapped_song['file'] = song.get('fileKey')
            mapped_song['other'] = {k: v for k, v in song.items() if k not in core_fields and k not in ['fileKey', 'artistId', 'otherArtistIds']}

            artist = artists_table.get_item(Key={'artistId': song['artistId']}).get('Item')
            mapped_song['artist'] = {
                'artistId': artist['artistId'],
                'name': artist['name'],
            } if artist else {}

            other_artists = _get_artists_by_ids(song.get('otherArtistIds', []))
            mapped_song['otherArtists'] = [
                {
                    'artistId': artist['artistId'],
                    'name': artist['name'],
                } for artist in other_artists
            ]

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


def _get_artists_by_ids(artist_ids):
    keys = [{'artistId': artist_id} for artist_id in artist_ids]

    response = dynamodb.batch_get_item(
        RequestItems={
            artists_table.name: {'Keys': keys}
        }
    )

    items = response.get('Responses', {}).get(artists_table.name, [])
    deserialized = [{k: list(v.values())[0] for k, v in item.items()} for item in items]

    return deserialized
