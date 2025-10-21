import os
import boto3
import json

s3 = boto3.client("s3")
BUCKET = os.environ['BUCKET']

dynamodb = boto3.resource('dynamodb', region_name=os.environ["REGION"])
genres_table = dynamodb.Table(os.environ['GENRES_TABLE'])

def lambda_handler(event, context):
    path_params = event.get("pathParameters") or {}
    file_key_param = path_params.get("fileKey")

    if not file_key_param:
        return {
            "statusCode": 400,
            "headers": _cors_headers(),
            "body": json.dumps({"message": "Missing fileKey"})
        }

    file_key = f"albums/{file_key_param}"

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
    }
