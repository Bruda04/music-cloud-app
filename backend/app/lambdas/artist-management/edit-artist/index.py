import json
import boto3
from datetime import datetime
import os

dynamodb = boto3.resource('dynamodb', region_name=os.environ["REGION"])
artists_table = dynamodb.Table(os.environ["ARTISTS_TABLE"])
genres_table = dynamodb.Table(os.environ["GENRES_TABLE"])
genre_contents_table = dynamodb.Table(os.environ["GENRE_CONTENTS_TABLE"])

def lambda_handler(event, context):
    try:
        claims = event.get("requestContext", {}).get("authorizer", {}).get("claims", {})
        if not claims.get("cognito:groups") or "Admins" not in claims.get("cognito:groups"):
            return _response(403, {"message": "Forbidden: Admins only"})

        body = json.loads(event.get("body", "{}"))
        artist_id = body.get("artistId", "").strip()
        name = body.get("name", "").strip()
        bio = body.get("bio", "").strip()
        genres = [g.strip().lower() for g in body.get("genres", []) if g.strip()]

        if not artist_id:
            return _response(400, {"error": "artistId is required for editing"})
        if not name or not bio or not genres:
            return _response(400, {"error": "Name, Bio and at least one Genre are required"})

        existing_artist = artists_table.get_item(Key={"artistId": artist_id}).get("Item")
        if not existing_artist:
            return _response(404, {"error": "Artist not found"})

        for genre in genres:
            try:
                genres_table.put_item(
                    Item={"genreName": genre},
                    ConditionExpression="attribute_not_exists(#g)",
                    ExpressionAttributeNames={"#g": "genreName"}
                )
            except genres_table.meta.client.exceptions.ConditionalCheckFailedException:
                pass

            genre_contents_table.put_item(
                Item={
                    "genreName": genre,
                    "contentKey": f"artist#{artist_id}"
                }
            )

        updated_item = {
            "name": name,
            "bio": bio,
            "genres": genres,
            "updatedAt": datetime.utcnow().isoformat()
        }

        if 'other' in body and isinstance(body['other'], dict):
            for k, v in body['other'].items():
                if k not in updated_item:
                    updated_item[k] = v
                else:
                    updated_item[f'other_{k}'] = v

        update_expr = "SET " + ", ".join(f"{k} = :{k}" for k in updated_item.keys())
        expr_attr_vals = {f":{k}": v for k, v in updated_item.items()}

        artists_table.update_item(
            Key={"artistId": artist_id},
            UpdateExpression=update_expr,
            ExpressionAttributeValues=expr_attr_vals
        )

        return _response(200, {"message": "Artist updated successfully", "artistId": artist_id})

    except Exception as e:
        return _response(500, {"error": str(e)})


def _response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps(body)
    }
