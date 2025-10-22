import decimal
import json
import boto3
import os
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb', region_name=os.environ["REGION"])
artists_table = dynamodb.Table(os.environ["ARTISTS_TABLE"])
albums_table = dynamodb.Table(os.environ["ALBUMS_TABLE"])
songs_table = dynamodb.Table(os.environ["SONGS_TABLE"])

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)

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
        artist_id = event.get('pathParameters', {}).get('artistId')

        if not artist_id:
            return _response(400, {'error': 'artistId is required'})

        artist = artists_table.get_item(Key={'artistId': artist_id}).get('Item')
        if not artist or artist.get('isDeleted', False):
            return _response(200, {
                'albums': [],
                'songs': [],
                'error': 'unknown artist'
            })

        albums_response = albums_table.query(
            KeyConditionExpression=Key('artistId').eq(artist_id)
        )
        albums = albums_response.get('Items', [])

        albums_result = []

        for item in albums:
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


















        songs_response = songs_table.query(
            KeyConditionExpression=Key('artistId').eq(artist_id)
        )
        songs = songs_response.get('Items', [])
        songs_result = []
        for item in songs:
            if item.get('isDeleted', False):
                continue
            songs_result.append({"artistId": item.get("artistId"), "name": item.get("name")})


        return _response(200, {
            'albums': albums_result,
            'songs': songs_result
        })

    except Exception as e:
        return _response(500, {'error': str(e)})

def _response(status_code, body):
    return {
        'statusCode': status_code,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': '*',
            'Content-Type': 'application/json'
        },
        'body': json.dumps(body, cls=DecimalEncoder)
    }
