import boto3
import os

USER_POOL_ID = os.environ['USER_POOL_ID']
GROUP_NAME = os.environ['GROUP_NAME']

cognito_client = boto3.client('cognito-idp')

def lambda_handler(event, context):
    try:
        username = event['userName']

        response = cognito_client.admin_add_user_to_group(
            UserPoolId=USER_POOL_ID,
            Username=username,
            GroupName=GROUP_NAME
        )

        print(f"User {username} added to group {GROUP_NAME}")
    except Exception as e:
        print(f"Error adding user to group: {str(e)}")

    return event
