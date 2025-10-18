import boto3
import os

GROUP_NAME = os.environ['GROUP_NAME']

cognito_client = boto3.client('cognito-idp')

def lambda_handler(event, context):
    try:
        username = event['userName']
        user_pool_id = event.get('userPoolId')

        response = cognito_client.admin_add_user_to_group(
            UserPoolId=user_pool_id,
            Username=username,
            GroupName=GROUP_NAME
        )

        print(f"User {username} added to group {GROUP_NAME}")
    except Exception as e:
        print(f"Error adding user to group: {str(e)}")

    return event
