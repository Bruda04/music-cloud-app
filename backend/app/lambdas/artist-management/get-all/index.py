import json
import os
import decimal
import boto3

dynamodb = boto3.resource('dynamodb', region_name=os.environ["REGION"])
artists_table = dynamodb.Table(os.environ["ARTISTS_TABLE"])

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
        limit = int(event.get('queryStringParameters', {}).get('limit', 10))
        last_key = event.get('queryStringParameters', {}).get('lastKey', None)

        scan_kwargs = {'Limit': limit}
        if last_key:
            scan_kwargs['ExclusiveStartKey'] = json.loads(last_key)

        scan_kwargs['FilterExpression'] = "attribute_not_exists(isDeleted) OR isDeleted = :false"
        scan_kwargs['ExpressionAttributeValues'] = {":false": False}

        response = artists_table.scan(**scan_kwargs)
        items = response.get('Items', [])
        items = convert_sets_to_lists(items)

        result = {
            'artists': items,
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
