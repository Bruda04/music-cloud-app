import json
import os
import decimal
import boto3

dynamodb = boto3.resource('dynamodb', region_name=os.environ["REGION"])
artists_table = dynamodb.Table(os.environ["ARTISTS_TABLE"])
gsi_deleted = os.environ["ARTISTS_TABLE_GSI_DELETED"]

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
        params = event.get("queryStringParameters") or {}



        # If no query params → return all non-deleted artists
        if not params:
            response = artists_table.query(
                IndexName=gsi_deleted,
                KeyConditionExpression=boto3.dynamodb.conditions.Key('isDeleted').eq(0),
                ProjectionExpression="artistId",
            )

            artist_keys = response.get('Items', [])
            artists = []
            for key in artist_keys:
                artist_id = key['artistId']
                artist_item = artists_table.get_item(Key={'artistId': artist_id}).get('Item')
                if artist_item:
                    artists.append(convert_sets_to_lists(artist_item))

            return {
                'statusCode': 200,
                'headers': {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Headers": "*",
                    "Content-Type": "application/json"
                },
                'body': json.dumps({'artists': artists}, cls=DecimalEncoder)
            }


        limit = int(params.get('limit', 10))
        last_key = params.get('lastKey')

        query_kwargs = {
            "IndexName": gsi_deleted,
            "KeyConditionExpression": boto3.dynamodb.conditions.Key("isDeleted").eq(0),
            "Limit": limit
        }

        if last_key:
            query_kwargs['ExclusiveStartKey'] = json.loads(last_key)

        response = artists_table.query(**query_kwargs)

        artist_keys = response.get('Items', [])
        artists = []
        for key in artist_keys:
            artist_id = key['artistId']
            artist_item = artists_table.get_item(Key={'artistId': artist_id}).get('Item')
            if artist_item:
                artists.append(convert_sets_to_lists(artist_item))

        result = {
            'artists': artists,
            'lastKey': json.dumps(response.get('LastEvaluatedKey'), cls=DecimalEncoder)
                       if 'LastEvaluatedKey' in response else None
        }

        return {
            'statusCode': 200,
            'headers': {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "OPTIONS,GET",
                "Content-Type": "application/json"
            },
            'body': json.dumps(result, cls=DecimalEncoder)
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': f'Failed to fetch artists: {str(e)}'})
        }
