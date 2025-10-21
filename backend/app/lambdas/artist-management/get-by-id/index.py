import json
import os
import decimal
import boto3

dynamodb = boto3.resource('dynamodb', region_name=os.environ["REGION"])
artists_table = dynamodb.Table(os.environ["ARTISTS_TABLE"])

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
        # Uzimamo artistId iz path parametara
        artist_id = event.get('pathParameters', {}).get('artistId')
        if not artist_id:
            return {
                'statusCode': 400,
                'headers': {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Headers": "*",
                    "Access-Control-Allow-Methods": "OPTIONS,GET",
                    "Content-Type": "application/json"
                },
                'body': json.dumps({'message': 'artistId is required'})
            }

        # Čitamo artista iz DynamoDB
        response = artists_table.get_item(Key={'artistId': artist_id})
        artist = response.get('Item')

        if not artist:
            return {
                'statusCode': 404,
                'headers': {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Headers": "*",
                    "Access-Control-Allow-Methods": "OPTIONS,GET",
                    "Content-Type": "application/json"
                },
                'body': json.dumps({'message': f'Artist with ID {artist_id} not found'})
            }

        # Konverzija svih setova u liste da JSON ne puca
        artist = convert_sets_to_lists(artist)

        return {
            'statusCode': 200,
            'headers': {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "OPTIONS,GET",
                "Content-Type": "application/json"
            },
            'body': json.dumps({'artist': artist}, cls=DecimalEncoder)
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "OPTIONS,GET",
                "Content-Type": "application/json"
            },
            'body': json.dumps({'message': f'Failed to fetch artist: {str(e)}'})
        }
