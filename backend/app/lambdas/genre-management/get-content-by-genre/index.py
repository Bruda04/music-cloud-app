import decimal
import json
import boto3
import os
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb', region_name=os.environ["REGION"])
genre_content_table = dynamodb.Table(os.environ["GENRE_CONTENT_TABLE"])
artists_table = dynamodb.Table(os.environ["ARTISTS_TABLE"])
albums_table = dynamodb.Table(os.environ["ALBUMS_TABLE"])

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)

def fetch_artist(artist_id, fetched_artists):
    if not artist_id:
        return None
    if artist_id in fetched_artists:
        return fetched_artists[artist_id]
    resp = artists_table.get_item(Key={'artistId': artist_id})
    artist = resp.get('Item')
    if artist:
        if artist.get('isDeleted', False):
            artist_obj = {'artistId': 'Unknown-artist', 'name': 'Unknown Artist'}
            fetched_artists[artist_id] = artist_obj
            return artist_obj
        artist_obj = {'artistId': artist['artistId'], 'name': artist.get('name', '')}
        fetched_artists[artist_id] = artist_obj
        return artist_obj
    return None

def lambda_handler(event, context):
    try:
        genre = event.get('pathParameters', {}).get('genreName')
        if not genre:
            return _response(400, {'error': 'Genre name is required'})

        response = genre_content_table.query(
            KeyConditionExpression=Key('genreName').eq(genre)
        )

        items = response.get('Items', [])
        if not items:
            return _response(200, {"artists": [], "albums": [], "message": "No content found for the specified genre."})

        content_keys = [item['contentKey'] for item in items if 'contentKey' in item]

        artist_keys = {key.split("#")[1] for key in content_keys if key.startswith('artist#')}
        album_keys = {(key.split("#")[1], key.split("#")[2]) for key in content_keys if key.startswith('album#')}

        request_items = {}

        if artist_keys:
            request_items[artists_table.name] = {'Keys': [{'artistId': k} for k in artist_keys]}
        if album_keys:
            request_items[albums_table.name] = {'Keys': [{'artistId': a, 'albumId': b} for (a, b) in album_keys]}

        batch_response = {}
        if request_items:
            batch_response = dynamodb.batch_get_item(RequestItems=request_items)

        artists = batch_response.get('Responses', {}).get(artists_table.name, [])
        albums = batch_response.get('Responses', {}).get(albums_table.name, [])

        artists = list({a['artistId']: a for a in artists}.values())
        albums = list({a['albumId']: a for a in albums}.values())
        final_albums = get_albums(albums)


        fetched_artists = {a['artistId']: a for a in artists}

        final_artists = []
        for artist_id in artist_keys:
            artist = next((a for a in artists if a['artistId'] == artist_id), None)
            if not artist or artist.get('isDeleted', False):
                continue
            else:
                clean_artist = {k: v for k, v in artist.items() if k not in ['createdAt']}
                final_artists.append(clean_artist)


        return _response(200, {
            "artists": final_artists,
            "albums": final_albums
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


def get_albums(albums) :
    # Prepare full album objects with the same structure as in get all albums
    result_albums = []
    for album in albums:
        core_fields = ['albumId', 'title', 'genres', 'imageFile']
        mapped_album = {key: album.get(key, '' if key != 'genres' else []) for key in core_fields}
        mapped_album['details'] = album.get('details', '')


        # Add other fields (anything not in the core fields)
        mapped_album['other'] = {k: v for k, v in album.items() if k not in core_fields and k not in ['artistId', 'tracks', 'otherArtistIds', 'details']}

        # Attach main artist info
        mapped_album['artist'] = get_artist_safe(album.get('artistId'))

        # Enrich tracks
        enriched_tracks = []
        for track in album.get('tracks', []):
            track_data = {
                'songId': track.get('songId'),
                'title': track.get('title'),
                'fileKey': track.get('fileKey'),
                'artistId': track.get('artistId'),
                'genres': track.get('genres', []),
                'ratingSum': track.get('ratingSum', 0),
                'ratingCount': track.get('ratingCount', 0),
                'lyrics': track.get('lyrics', ''),
            }

            # Add artist info
            track_data['artist'] = get_artist_safe(track.get('artistId'))

            # Add other artists info
            other_artists = _get_artists_by_ids(track.get('otherArtistIds', []))
            track_data['otherArtists'] = [get_artist_safe(a.get('artistId')) for a in other_artists]

            enriched_tracks.append(track_data)

        mapped_album['tracks'] = enriched_tracks

        result_albums.append(mapped_album)
    return result_albums


def get_artist_safe(artist_id):
    """Get artist or return 'Unknown Artist' if its deleted or doesn't exist."""
    try:
        artist = artists_table.get_item(Key={'artistId': artist_id}).get('Item')
        if not artist or artist.get('isDeleted', 1):
            return {"artistId": "unknown-artist", "name": "Unknown Artist"}
        return {"artistId": artist.get("artistId", ""), "name": artist.get("name", "Unknown Artist")}
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
        if item.get('isDeleted', 1) == 1:
            continue
        result.append({"artistId": item.get("artistId"), "name": item.get("name")})
    return result
