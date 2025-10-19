import json
import os
import boto3

dynamodb = boto3.resource('dynamodb', region_name=os.environ["REGION"])
subscriptions_table = dynamodb.Table(os.environ["SUBSCRIPTIONS_TABLE"])
ses_client = boto3.client('ses', region_name=os.environ["REGION"])
from_email = os.environ["SES_FROM_EMAIL"]

def lambda_handler(event, context):
    try:
        for record in event.get('Records', []):
            body = json.loads(record['body'])
            content_type = body['contentType']
            content_id = body['contentId']
            metadata = body['metadata']  # {from: artist_name, contentName: name_of_content}

            artist_name = metadata.get('from', 'Unknown Artist')
            content_name = metadata.get('contentName', 'Unknown Content')

            match content_type:
                case 'genre':
                    email_subject = f"New in genre {content_id.upper()}"
                    email_body = f"Hello!\n\nA new song has been released in genre {content_id.upper()}.\n\n" \
                                 f"Title: {content_name}\nBy: {artist_name}\n\n" \
                                 f"Check it out on our platform!"
                case 'artist':
                    email_subject = f"New from artist {artist_name}"
                    email_body = f"Hello!\n\nA new song has been released by {artist_name}.\n\n" \
                                 f"Title: {content_name}\n \n" \
                                 f"Check it out on our platform!"
                case _:
                    continue



            subscribers = get_subscribers(content_type, content_id)
            for user_email in subscribers:
                send_email(user_email, email_body, email_subject)

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Notifications sent successfully'})
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

def get_subscribers(content_type, content_id):
    content_key = f"{content_type}#{content_id}"
    response = subscriptions_table.query(
        KeyConditionExpression=boto3.dynamodb.conditions.Key('contentKey').eq(content_key)
    )
    subscribers = [item['user'] for item in response.get('Items', [])]
    return subscribers

def send_email(target_email, content, title):
    ses_client.send_email(
        Source=from_email,
        Destination={"ToAddresses": [target_email]},
        Message={
            "Subject": {"Data": title},
            "Body": {"Text": {"Data": content}}
        }
    )