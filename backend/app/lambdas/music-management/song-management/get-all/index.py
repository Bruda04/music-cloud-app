import json
import os
import decimal
import boto3

dynamodb = boto3.resource('dynamodb', region_name=os.environ["REGION"])
songs_table = dynamodb.Table(os.environ['SONGS_TABLE'])
artists_table = dynamodb.Table(os.environ['ARTISTS_TABLE'])

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)

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

            mapped_song['artist'] = get_artist_safe(song.get('artistId'))
            other_artists = _get_artists_by_ids(song.get('otherArtistIds', []))
            mapped_song['otherArtists'] = [get_artist_safe(a.get('artistId')) for a in other_artists]

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
            'body': json.dumps(result, cls=DecimalEncoder)
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': f'Failed to fetch songs: {str(e)}'})
        }

def get_artist_safe(artist_id):
    """Get artist from DynamoDB, return 'Unknown Artist' if not found or deleted"""
    if not artist_id:
        return {"artistId": "unknown-artist", "name": "Unknown Artist"}
    try:
        artist = artists_table.get_item(Key={'artistId': artist_id}).get('Item')
        if not artist or artist.get('isDeleted', False):
            return {"artistId": "unknown-artist", "name": "Unknown Artist"}
        return {"artistId": artist.get('artistId', 'unknown-artist'), "name": artist.get('name', 'Unknown Artist')}
    except Exception:
        return {"artistId": "unknown-artist", "name": "Unknown Artist"}

def _get_artists_by_ids(artist_ids):
    """Batch get artists iz DynamoDB, bez obrisanih umetnika"""
    if not artist_ids:
        return []

    keys = [{'artistId': artist_id} for artist_id in artist_ids]

    response = dynamodb.batch_get_item(
        RequestItems={
            artists_table.name: {'Keys': keys}
        }
    )

    items = response.get('Responses', {}).get(artists_table.name, [])
    result = []
    for item in items:
        if item.get('isDeleted', False):
            continue
        result.append({"artistId": item.get("artistId"), "name": item.get("name")})
    return result
