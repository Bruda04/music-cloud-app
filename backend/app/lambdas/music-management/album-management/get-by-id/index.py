import json
import boto3
import os
from boto3.dynamodb.conditions import Key
from decimal import Decimal

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            if o % 1 == 0:
                return int(o)
            else:
                return float(o)
        return super(DecimalEncoder, self).default(o)

dynamodb = boto3.resource('dynamodb', region_name=os.environ["REGION"])
albums_table = dynamodb.Table(os.environ['ALBUMS_TABLE'])
albums_table_gsi_id = os.environ['ALBUMS_TABLE_GSI_ID']
artists_table = dynamodb.Table(os.environ['ARTISTS_TABLE'])

def get_artist_safe(artist_id):
    """Get artist or return 'Unknown Artist' if its deleted or doesn't exist."""
    try:
        artist = artists_table.get_item(Key={'artistId': artist_id}).get('Item')
        if not artist or artist.get('isDeleted', False):
            return {"artistId": "unknown-artist", "name": "Unknown Artist"}
        return {"artistId": artist.get("artistId", ""), "name": artist.get("name", "Unknown Artist")}
    except Exception:
        return {"artistId": "unknown-artist", "name": "Unknown Artist"}

def lambda_handler(event, context):
    album_id = event.get('pathParameters', {}).get('id')
    
    if not album_id:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Missing albumId in path"}, cls=DecimalEncoder)
        }

    try:
        gsi_response = albums_table.query(
            IndexName=albums_table_gsi_id,
            KeyConditionExpression=Key('albumId').eq(album_id)
        )

        if not gsi_response['Items']:
            return {
                "statusCode": 404,
                "body": json.dumps({"message": "Album not found"}, cls=DecimalEncoder)
            }

        artist_id = gsi_response['Items'][0]['artistId']

        response = albums_table.get_item(Key={'albumId': album_id, 'artistId': artist_id})
        item = response.get('Item')

        if not item:
            return {
                "statusCode": 404,
                "body": json.dumps({"message": "Album not found"}, cls=DecimalEncoder)
            }

        fetched_artists = {}

        artist = get_artist_safe(item['artistId'])
        fetched_artists[artist["artistId"]] = artist

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

        reserved_keys = {"albumId", "title", "artistId", "genres", "tracks", "details", "imageFile"}
        album["other"] = {k: v for k, v in item.items() if k not in reserved_keys}

        return {
            "statusCode": 200,
            "body": json.dumps(album, cls=DecimalEncoder),
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Content-Type": "application/json"
            }
        }
        
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"message": f"Internal server error: {str(e)}"}, cls=DecimalEncoder),
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Content-Type": "application/json"
            }
        }
