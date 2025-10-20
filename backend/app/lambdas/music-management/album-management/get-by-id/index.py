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

        album = {
            "albumId": item.get("albumId"),
            "title": item.get("title"),
            "artistId": item.get("artistId", []),
            "genres": item.get("genres", []),
            "tracks": item.get("tracks", []),
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
