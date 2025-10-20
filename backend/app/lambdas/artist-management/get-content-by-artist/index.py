import json
import boto3
import os

from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb', region_name=os.environ["REGION"])
albums_table = dynamodb.Table(os.environ["ALBUMS_TABLE"])
songs_table = dynamodb.Table(os.environ["SONGS_TABLE"])

def lambda_handler(event, context):
    try:
        artist_id = event['pathParameters']['artistId']

        if not artist_id:
            return {
                'statusCode': 400,
                'headers': {'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({'error': 'artistId is required'})
            }

        albums_response = albums_table.query(
            KeyConditionExpression=Key('artistId').eq(artist_id)
        )
        albums = albums_response.get('Items', [])
        skip_keys = []
        albums = [{k: v for k, v in album.items() if k not in skip_keys} for album in albums]

        songs_response = songs_table.query(
            KeyConditionExpression=Key('artistId').eq(artist_id)
        )
        songs = songs_response.get('Items', [])
        skip_keys = []
        songs = [{k: v for k, v in song.items() if k not in skip_keys} for song in songs]

        return {
            'statusCode': 200,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({
                'albums': albums,
                'songs': songs
            })
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': str(e)})
        }
