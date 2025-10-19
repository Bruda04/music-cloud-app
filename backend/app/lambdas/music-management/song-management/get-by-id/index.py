import json
from http.client import responses

import boto3
import os

from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb', region_name=os.environ["REGION"])
songs_table = dynamodb.Table(os.environ['SONGS_TABLE'])
songs_table_sgi_id = os.environ['SONGS_TABLE_GSI_ID']


def lambda_handler(event, context):
    try:
        song_id = event.get('pathParameters', {}).get('id')
        if not song_id:
            return {
                'statusCode': 400,
                'headers': _cors_headers(),
                'body': json.dumps({'message': 'Missing songId in path parameters'})
            }

        song_keys = songs_table.query(
            IndexName= songs_table_sgi_id,
            KeyConditionExpression=Key("songId").eq(song_id)
        )

        if song_keys['Count'] == 0 or song_keys['Items'] is None:
            return {
                'statusCode': 404,
                'headers': _cors_headers(),
                'body': json.dumps({'message': 'Song not found'})
            }

        response = songs_table.get_item(Key={'songId': song_id, "artistId": song_keys['Items']['artistId']})
        item = response.get('Item')
        if not item:
            return {
                'statusCode': 404,
                'headers': _cors_headers(),
                'body': json.dumps({'message': 'Song not found'})
            }

        core_fields = ['songId', 'title', 'genres', 'artistId', 'otherArtistsIds']
        mapped_song = {key: item.get(key, '' if key not in ['genres', 'otherArtistsIds'] else []) for key in core_fields}
        mapped_song['file'] = item.get('fileKey')
        mapped_song['other'] = {k: v for k, v in item.items() if k not in core_fields and k != 'fileKey'}

        return {
            'statusCode': 200,
            'headers': _cors_headers(),
            'body': json.dumps(mapped_song)
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'headers': _cors_headers(),
            'body': json.dumps({'message': f'Failed to fetch song: {str(e)}'})
        }


def _cors_headers():
    return {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "*",
        "Access-Control-Allow-Methods": "OPTIONS,GET",
        "Content-Type": "application/json"
    }
