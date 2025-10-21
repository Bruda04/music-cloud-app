import json
import boto3
import os
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb', region_name=os.environ["REGION"])
artists_table = dynamodb.Table(os.environ["ARTISTS_TABLE"])
albums_table = dynamodb.Table(os.environ["ALBUMS_TABLE"])
songs_table = dynamodb.Table(os.environ["SONGS_TABLE"])

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

        songs_response = songs_table.query(
            KeyConditionExpression=Key('artistId').eq(artist_id)
        )
        songs = songs_response.get('Items', [])

        return _response(200, {
            'albums': albums,
            'songs': songs
        })

    except Exception as e:
        return _response(500, {'error': str(e)})

def _response(status_code, body):
    return {
        'statusCode': status_code,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,GET',
            'Content-Type': 'application/json'
        },
        'body': json.dumps(body)
    }
