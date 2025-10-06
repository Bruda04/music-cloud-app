import json
import boto3
import uuid
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Artists') 

#TODO: check if user making artist has role: admin
def lambda_handler(event, context):
    if event["httpMethod"] == "OPTIONS":
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
            },
            "body": ""
        }

    try:
        body = json.loads(event.get("body", "{}"))

        name = body.get("name", "").strip()
        bio = body.get("bio", "").strip()
        genres = body.get("genres", [])

        if not name or not bio or not genres:
            return {
                "statusCode": 400,
                "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Headers": "*",
                    "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
                    "Content-Type": "application/json"
                },
                "body": json.dumps({"error": "Name, Bio and at least one Genre are required"})
            }

        artist_id = str(uuid.uuid4())
        created_at = datetime.utcnow().isoformat()

        item = {
            "artistId": artist_id,
            "name": name,
            "bio": bio,
            "genres": genres,
            "isDeleted": False,
            "createdAt": created_at
        }

        table.put_item(Item=item)

        return {
            "statusCode": 201,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
                "Content-Type": "application/json"
            },
            "body": json.dumps({"message": "Artist created", "artist": item})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
                "Content-Type": "application/json"
            },
            "body": json.dumps({"error": str(e)})
        }
