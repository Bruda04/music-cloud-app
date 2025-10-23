import json
import boto3
import os

dynamodb = boto3.resource('dynamodb', region_name=os.environ["REGION"])
artists_table = dynamodb.Table(os.environ["ARTISTS_TABLE"])

def lambda_handler(event, context):
    try:
        claims = event.get("requestContext", {}).get("authorizer", {}).get("claims", {})
        if not claims.get("cognito:groups") or "Admins" not in claims.get("cognito:groups"):
            return _response(403, {"message": "Forbidden: Admins only"})

        artist_id = event.get("pathParameters", {}).get("artistId")
        if not artist_id:
            return _response(400, {"message": "Missing artistId in path parameters"})

        existing = artists_table.get_item(Key={"artistId": artist_id})
        if "Item" not in existing:
            return _response(404, {"message": "Artist not found"})

        artists_table.update_item(
            Key={"artistId": artist_id},
            UpdateExpression="SET isDeleted = :val",
            ExpressionAttributeValues={":val": 1}
        )

        return _response(200, {"message": f"Artist {artist_id} marked as deleted"})

    except Exception as e:
        return _response(500, {"error": str(e)})


def _response(status_code, body):
    """Helper za dosledan odgovor"""
    return {
        "statusCode": status_code,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET,DELETE",
            "Content-Type": "application/json"
        },
        "body": json.dumps(body)
    }
