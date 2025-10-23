import datetime
import decimal
import json
import os
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb', region_name=os.environ["REGION"])
user_feed_table = dynamodb.Table(os.environ["USER_FEED_TABLE"])
songs_table = dynamodb.Table(os.environ['SONGS_TABLE'])
songs_table_gsi_id = os.environ['SONGS_TABLE_GSI_ID']
albums_table = dynamodb.Table(os.environ['ALBUMS_TABLE'])
albums_table_gsi_id = os.environ['ALBUMS_TABLE_GSI_ID']
artists_table = dynamodb.Table(os.environ['ARTISTS_TABLE'])

MAX_FEED_ITEMS = 20

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
        claims = event.get("requestContext", {}).get("authorizer", {}).get("claims", {})
        user = claims.get("email")
        if not user:
            return {'statusCode': 400, 'body': json.dumps({'error': 'User email not found in token'}, cls=DecimalEncoder), 'headers': _cors_headers()}

        resp = user_feed_table.query(
            KeyConditionExpression=Key('user').eq(user),
            Limit=MAX_FEED_ITEMS,
            ScanIndexForward=False
        )
        items = resp.get('Items', [])
        if not items:
            return {'statusCode': 200, 'body': json.dumps({'songs': [], 'albums': []}), 'headers': _cors_headers()}

        timestamps = [datetime.datetime.fromisoformat(i['timestamp']) for i in items]
        newest = max(timestamps)
        oldest = min(timestamps)
        time_range = (newest - oldest).total_seconds() or 1

        songs = []
        albums = []
        fetched_artists = {}

        for i in items:
            ts = datetime.datetime.fromisoformat(i['timestamp'])
            time_weight = (ts - oldest).total_seconds() / time_range
            s = float(i.get('score', 0))
            weighted_score = s * 0.7 + time_weight * 0.3

            content_key = i['contentKey']

            # fetch full entity
            entity = None
            if content_key.startswith('song#'):
                song_id = content_key.split('#', 1)[1]
                resp = songs_table.query(
                    IndexName=songs_table_gsi_id,
                    KeyConditionExpression=Key('songId').eq(song_id),
                    Limit=1
                )
                items = resp.get('Items', [])
                if items:
                    pk = items[0]['artistId']
                    if not pk:
                        continue
                    entity = songs_table.get_item(Key={'artistId': pk, 'songId': song_id}).get('Item')

            elif content_key.startswith('album#'):
                album_id = content_key.split('#', 1)[1]
                resp = albums_table.query(
                    IndexName=albums_table_gsi_id,
                    KeyConditionExpression=Key('albumId').eq(album_id),
                    Limit=1
                )
                items = resp.get('Items', [])
                if items:
                    pk = items[0]['artistId']
                    if not pk:
                        continue
                    entity = albums_table.get_item(Key={'albumId': album_id, 'artistId': pk}).get('Item')

            if not entity:
                continue

            # replace artistIds with artist objects
            artist_id = entity.get('artistId')
            artist_entity = fetch_artist(artist_id, fetched_artists)
            entity['artist'] =  artist_entity if artist_entity else {'artistId': 'Unknown-artist', 'name': 'Unknown Artist'}
            entity.pop('artistId', None)

            if 'otherArtistIds' in entity:
                other_artist_objs = []
                for other_id in entity['otherArtistIds']:
                    other_artist = fetch_artist(other_id, fetched_artists)
                    if other_artist:
                        other_artist_objs.append(other_artist)
                    else:
                        other_artist_objs.append({'artistId': 'Unknown-artist', 'name': 'Unknown Artist'})
                entity['otherArtists'] = other_artist_objs
                entity.pop('otherArtistIds', None)

            entity.update({
                'weighted_score': weighted_score,
            })

            if content_key.startswith('song#'):
                songs.append(entity)
            elif content_key.startswith('album#'):
                albums.append(entity)

        # sort by weighted_score
        songs.sort(key=lambda x: x['weighted_score'], reverse=True)
        albums.sort(key=lambda x: x['weighted_score'], reverse=True)

        return {'statusCode': 200,
                'headers': _cors_headers(),
                'body': json.dumps({'songs': songs, 'albums': albums}, cls=DecimalEncoder)}

    except Exception as e:
        return {'statusCode': 500,
                'headers': _cors_headers(),
                'body': json.dumps({'error': str(e)}, cls=DecimalEncoder)}

def _cors_headers():
    return {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "*",
        "Content-Type": "application/json"
    }