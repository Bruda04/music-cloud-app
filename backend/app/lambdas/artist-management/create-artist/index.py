import json
import boto3
import uuid
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
artists_table = dynamodb.Table('Artists') 
genres_table = dynamodb.Table('Genres') 

#TODO: check if user making artist has role: admin
def lambda_handler(event, context):
    try:
        body = json.loads(event.get("body", "{}"))

        name = body.get("name", "").strip()
        bio = body.get("bio", "").strip()
        genres = [g.strip() for g in body.get("genres", []) if g.strip()]

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

        for genre in genres:
            try:
                genres_table.put_item(
                    Item={"genreName": genre.lower()},
                    ConditionExpression="attribute_not_exists(#g)",
                    ExpressionAttributeNames={"#g": "genreName"}
                )
            except genres_table.meta.client.exceptions.ConditionalCheckFailedException:
                pass


        artist_id = str(uuid.uuid4())
        created_at = datetime.utcnow().isoformat()

        item = {
            "artistId": artist_id,
            "name": name,
            "bio": bio,
            "genres":  [g.lower() for g in genres if g] ,
            "isDeleted": False,
            "createdAt": created_at
        }

        artists_table.put_item(Item=item)

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
