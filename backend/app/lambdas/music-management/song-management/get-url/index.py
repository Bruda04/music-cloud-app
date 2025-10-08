import boto3
import json

s3 = boto3.client("s3")
BUCKET = "music-app-content-dhox6eq69e"

def lambda_handler(event, context):
    path_params = event.get("pathParameters") or {}
    file_key = "songs/"+path_params.get("fileKey")

    if not file_key:
        return {
            "statusCode": 400,
            "headers": _cors_headers(),
            "body": json.dumps({"message": "Missing fileKey"})
        }

    try:
        url = s3.generate_presigned_url(
            ClientMethod="get_object",
            Params={"Bucket": BUCKET, "Key": file_key},
            ExpiresIn=3600
        )
        return {
            "statusCode": 200,
            "headers": _cors_headers(),
            "body": json.dumps({"url": url})
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": _cors_headers(),
            "body": json.dumps({"message": str(e)})
        }

def _cors_headers():
    return {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "*",
        "Access-Control-Allow-Methods": "OPTIONS,GET",
    }