import json
import os
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb', region_name=os.environ["REGION"])
subscriptions_table = dynamodb.Table(os.environ["SUBSCRIPTIONS_TABLE"])
subscriptions_table_gsi_id = os.environ["SUBSCRIPTIONS_TABLE_GSI_ID"]
artists_table = dynamodb.Table(os.environ["ARTISTS_TABLE"])

def lambda_handler(event, context):
    try:
        claims = event.get("requestContext", {}).get("authorizer", {}).get("claims", {})
        user = claims.get("email")

        if not user:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'User email not found in token'})
            }

        response = subscriptions_table.query(
            IndexName=subscriptions_table_gsi_id,
            KeyConditionExpression=Key('user').eq(user),
            ProjectionExpression="contentKey"
        )

        items = response.get("Items", [])

        artists = []
        artists_ids = []
        genres = []

        for item in items:
            content_key = item.get("contentKey", "")
            if content_key.startswith("artist#"):
                artists_ids.append(content_key.split("#", 1)[1])
            elif content_key.startswith("genre#"):
                genres.append(content_key.split("#", 1)[1])

        if artists_ids:
            for artist_id in artists_ids:
                artist_response = artists_table.get_item(Key={'artistId': artist_id})
                artist = artist_response.get('Item')
                if artist:
                    artists.append({
                        'artistId': artist['artistId'],
                        'name': artist['name'],
                    })

        return {
            'statusCode': 200,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({
                'artists': artists,
                'genres': genres
            })
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }