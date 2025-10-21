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
            # Fetch main artist
            artist_id = item.get('artistId')
            artist = {}
            if artist_id:
                artist = artists_table.get_item(Key={'artistId': artist_id}).get('Item', {})
            fetched_artists = {artist.get('artistId'): artist} if artist else {}

            tracks = []
            for t in item.get("tracks", []):
                other_artist_ids = t.get("otherArtistIds", [])
                # Fetch other artists
                for oid in other_artist_ids:
                    if oid not in fetched_artists:
                        fetched_artists[oid] = artists_table.get_item(Key={'artistId': oid}).get('Item', {})
                track = t.copy()
                track["artist"] = {"artistId": artist.get("artistId", ""), "name": artist.get("name", "")} if artist else {}
                track["otherArtists"] = [
                    {"id": fetched_artists[oid]["artistId"], "name": fetched_artists[oid]["name"]}
                    for oid in other_artist_ids
                    if oid in fetched_artists
                ]
                tracks.append(track)

            album = {
                "albumId": item.get("albumId"),
                "title": item.get("title"),
                "artist": {"artistId": artist.get("artistId", ""), "name": artist.get("name", "")} if artist else {},
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