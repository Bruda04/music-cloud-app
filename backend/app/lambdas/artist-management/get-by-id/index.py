import json
import os
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
artists_table = dynamodb.Table(os.environ['ARTISTS_TABLE'])

def lambda_handler(event, context):
    try:
        artist_id = event['pathParameters']['artistId']

        response = artists_table.get_item(Key={'artistId': artist_id})
        artist = response.get('Item')

        if not artist:
            return {
                'statusCode': 404,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Methods': 'GET'
                },
                'body': json.dumps({'message': 'Artist not found'})
            }

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'GET'
            },
            'body': json.dumps(artist)
        }

    except Exception as e:
        print(f"Error fetching artist: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'GET'
            },
            'body': json.dumps({'message': f"Error fetching artist: {str(e)}"})
        }