import json
import boto3
import os

dynamodb = boto3.resource('dynamodb', region_name=os.environ["REGION"])
albums_table = dynamodb.Table(os.environ['ALBUMS_TABLE'])

def lambda_handler(event, context):
    album_id = event.get('pathParameters', {}).get('id')
    
    if not album_id:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Missing albumId in path"})
        }

    try:
        response = albums_table.get_item(
            Key={'albumId': album_id}
        )
        
        item = response.get('Item')
        if not item:
            return {
                "statusCode": 404,
                "body": json.dumps({"message": "Album not found"})
            }
        
        album = {
            "albumId": item.get("albumId"),
            "title": item.get("title"),
            "artistIds": item.get("artistIds", []),
            "genres": item.get("genres", []),
            "tracks": item.get("tracks", []),
        }

        reserved_keys = {"albumId", "title", "artistIds", "genres", "tracks"}
        other = {k: v for k, v in item.items() if k not in reserved_keys}
        album["other"] = other

        return {
            "statusCode": 200,
            "body": json.dumps(album),
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Content-Type": "application/json"
            }
        }
        
    except Exception as e:
        print(f"Error fetching album: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Internal server error"}),
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Content-Type": "application/json"
            }
        }
