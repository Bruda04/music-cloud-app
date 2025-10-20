import json
import boto3
import os

from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb', region_name=os.environ["REGION"])
genre_content_table = dynamodb.Table(os.environ["GENRE_CONTENT_TABLE_NAME"])
artists_table = dynamodb.Table(os.environ["ARTISTS_TABLE_NAME"])
albums_table = dynamodb.Table(os.environ["ALBUMS_TABLE_NAME"])

def lambda_handler(event, context):
    try:
        genre = event['pathParameters']['genreName']

        if not genre:
            return {
                'statusCode': 400,
                'headers': {'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({'error': 'Genre name is required'})
            }

        response = genre_content_table.query(
            KeyConditionExpression=Key('genreName').eq(genre)
        )

        items = response.get('Items', [])
        if not items:
            return {
                'statusCode': 200,
                'body': json.dumps({"artists": [], "albums": []})
            }

        content_keys = items[0].get('contentKey', [])

        artist_keys = set([key.split("#")[1] for key in content_keys if key.startswith('artist#')])
        album_keys = {
            (key.split("#")[1], key.split("#")[2])  # (artistId, albumId)
            for key in content_keys if key.startswith('album#')
        }

        request_items = {}

        if artist_keys:
            request_items[artists_table.name] = {
                'Keys': [{'artistId': k} for k in artist_keys]
            }
        if album_keys:
            request_items[albums_table.name] = {
                'Keys': [{ 'artistId': a, 'albumId': b} for (a, b) in album_keys]
            }

        batch_response = {}
        if request_items:
            batch_response = dynamodb.batch_get_item(RequestItems=request_items)

        artists = batch_response.get('Responses', {}).get(artists_table.name, [])
        albums = batch_response.get('Responses', {}).get(albums_table.name, [])

        artists = list({a['artistId']: a for a in artists}.values())
        albums = list({a['albumId']: a for a in albums}.values())

        artists = [{k: v for k, v in artist.items() if k not in ["createdAt"]} for artist in artists]
        albums = [{k: v for k, v in album.items() if k not in ["createdAt", "tracks"]} for album in albums]

        return {
            'statusCode': 200,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({
                "artists": artists,
                "albums": albums
            })
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': str(e)})
        }
