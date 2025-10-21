import json
import boto3
import os
from decimal import Decimal
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb', region_name=os.environ["REGION"])
songs_table = dynamodb.Table(os.environ['SONGS_TABLE'])
songs_table_sgi_id = os.environ['SONGS_TABLE_GSI_ID']
artists_table = dynamodb.Table(os.environ['ARTISTS_TABLE'])
ratings_table = dynamodb.Table(os.environ['RATINGS_TABLE'])

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            if obj % 1 == 0:
                return int(obj)
            return float(obj)
        return super(DecimalEncoder, self).default(obj)


def lambda_handler(event, context):
    try:
        song_id = event.get('pathParameters', {}).get('id')
        if not song_id:
            return _response(400, {'message': 'Missing songId in path parameters'})

        song_keys = songs_table.query(
            IndexName=songs_table_sgi_id,
            KeyConditionExpression=Key("songId").eq(song_id)
        )

        if song_keys.get('Count', 0) == 0 or not song_keys.get('Items'):
            return _response(404, {'message': 'Song not found'})

        artist_id = song_keys['Items'][0]['artistId']

        response = songs_table.get_item(Key={'songId': song_id, 'artistId': artist_id})
        item = response.get('Item')
        if not item:
            return _response(404, {'message': 'Song not found'})

        core_fields = ['songId', 'title', 'genres', 'imageFile', 'lyrics']
        mapped_song = {key: item.get(key, [] if key == 'genres' else '') for key in core_fields}
        mapped_song['file'] = item.get('fileKey')
        mapped_song['other'] = {
            k: v for k, v in item.items()
            if k not in core_fields + ['fileKey', 'artistId', 'otherArtistIds', 'ratingSum', 'ratingCount']
        }
        mapped_song['rating'] = (
            item.get('ratingSum', 0) / item.get('ratingCount', 1)
            if item.get('ratingCount', 0) > 0 else 0
        )

        mapped_song['artist'] = get_artist_safe(artist_id)
        other_artists = _get_artists_by_ids(item.get('otherArtistIds', []))
        mapped_song['otherArtists'] = [get_artist_safe(a.get('artistId')) for a in other_artists]

        claims = event.get("requestContext", {}).get("authorizer", {}).get("claims", {})
        user = claims.get("email")
        can_rate = True
        if user:
            user_rating = ratings_table.get_item(Key={'user': user, 'contentKey': f"song#{song_id}"})
            can_rate = 'Item' not in user_rating

        mapped_song["canRate"] = can_rate

        return _response(200, mapped_song)

    except Exception as e:
        return _response(500, {'message': f'Failed to fetch song: {str(e)}'})


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
    if not artist_ids:
        return []
    keys = [{'artistId': artist_id} for artist_id in artist_ids]
    response = dynamodb.batch_get_item(
        RequestItems={artists_table.name: {'Keys': keys}}
    )
    items = response.get('Responses', {}).get(artists_table.name, [])
    return [item for item in items if not item.get('isDeleted', False)]


def _response(status_code, body):
    return {
        'statusCode': status_code,
        'headers': _cors_headers(),
        'body': json.dumps(body, cls=DecimalEncoder)
    }


def _cors_headers():
    return {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "*",
        "Access-Control-Allow-Methods": "OPTIONS,GET",
        "Content-Type": "application/json"
    }
