import json
import os
import decimal
import boto3

dynamodb = boto3.resource('dynamodb', region_name=os.environ["REGION"])
albums_table = dynamodb.Table(os.environ['ALBUMS_TABLE'])
artists_table = dynamodb.Table(os.environ['ARTISTS_TABLE'])

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)

def convert_sets_to_lists(obj):
    if isinstance(obj, set):
        return list(obj)
    elif isinstance(obj, dict):
        return {k: convert_sets_to_lists(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_sets_to_lists(i) for i in obj]
    else:
        return obj

def get_artist_safe(artist_id):
    """Get artist or return 'Unknown Artist' if its deleted or doesn't exist."""
    try:
        artist = artists_table.get_item(Key={'artistId': artist_id}).get('Item')
        if not artist or artist.get('isDeleted', 1):
            return {"artistId": "unknown-artist", "name": "Unknown Artist"}
        return {"artistId": artist.get("artistId", ""), "name": artist.get("name", "Unknown Artist")}
    except Exception:
        return {"artistId": "unknown-artist", "name": "Unknown Artist"}

def lambda_handler(event, context):
    try:
        limit = int(event.get('queryStringParameters', {}).get('limit', 10))
        last_key = event.get('queryStringParameters', {}).get('lastKey', None)

        scan_kwargs = {'Limit': limit}
        if last_key:
            scan_kwargs['ExclusiveStartKey'] = json.loads(last_key)

        response = albums_table.scan(**scan_kwargs)
        items = response.get('Items', [])
        items = convert_sets_to_lists(items)

        albums_result = []

        for item in items:
            artist_id = item.get('artistId')
            artist = get_artist_safe(artist_id) if artist_id else {"artistId": "unknown-artist", "name": "Unknown Artist"}
            fetched_artists = {artist["artistId"]: artist}
            tracks = []
            for t in item.get("tracks", []):
                other_artist_ids = t.get("otherArtistIds", [])
                other_artists = []
                for oid in other_artist_ids:
                    if oid not in fetched_artists:
                        fetched_artists[oid] = get_artist_safe(oid)
                    other_artists.append(fetched_artists[oid])
                track = t.copy()
                track["artist"] = artist
                track["otherArtists"] = other_artists
                tracks.append(track)

            album = {
                "albumId": item.get("albumId"),
                "title": item.get("title"),
                "artist": artist,
                "genres": item.get("genres", []),
                "tracks": tracks,
                "details": item.get("details", {}),
                "imageFile": item.get("imageFile", "")
            }

            albums_result.append(album)

        result = {
            'albums': albums_result,
            'lastKey': json.dumps(response.get('LastEvaluatedKey'), cls=DecimalEncoder)
                       if 'LastEvaluatedKey' in response else None
        }

        return {
            'statusCode': 200,
            'headers': {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
                "Content-Type": "application/json"
            },
            'body': json.dumps(result, cls=DecimalEncoder)
        }

    except Exception as e:
        return {
            'statusCode': 500,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*"
            },
            'body': json.dumps({'message': f'Failed to fetch albums: {str(e)}'})
        }