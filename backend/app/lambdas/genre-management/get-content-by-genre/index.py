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

        final_artists = []
        for artist_id in artist_keys:
            artist = next((a for a in artists if a['artistId'] == artist_id), None)
            if not artist or artist.get('isDeleted', False):
                final_artists.append({
                    'artistId': artist_id,
                    'name': 'Unknown Artist'
                })
            else:
                clean_artist = {k: v for k, v in artist.items() if k not in ['createdAt']}
                final_artists.append(clean_artist)

        final_albums = [
            {k: v for k, v in album.items() if k not in ['createdAt', 'tracks']}
            for album in albums
        ]

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
