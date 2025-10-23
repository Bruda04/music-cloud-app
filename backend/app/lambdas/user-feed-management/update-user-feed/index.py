import json
import os
from datetime import datetime
from decimal import Decimal

import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb', region_name=os.environ["REGION"])
user_feed_table = dynamodb.Table(os.environ["USER_FEED_TABLE"])
subscriptions_table = dynamodb.Table(os.environ["SUBSCRIPTIONS_TABLE"])
subscriptions_table_gsi_id = os.environ["SUBSCRIPTIONS_TABLE_GSI_ID"]
listening_history_table = dynamodb.Table(os.environ["LISTENING_HISTORY_TABLE"])
listening_history_table_gsi_artist_id = os.environ["LISTENING_HISTORY_TABLE_GSI_ARTIST_ID"]
ratings_table = dynamodb.Table(os.environ["RATINGS_TABLE"])
ratings_table_gsi_artist_id = os.environ["RATINGS_TABLE_GSI_ARTIST_ID"]


def lambda_handler(event, context):
    try:
        for record in event.get('Records', []):
            sns_message = json.loads(record['body'])
            message_str = sns_message['Message']
            body = json.loads(message_str)

            artist_id = body["artistId"]

            genres = body["genres"]
            album_id = body.get("albumId")
            song_id = body.get("songId")
            metadata = body["metadata"]
            content_type = metadata["contentType"]
            content_key = f"{content_type}#{song_id or album_id}"

            target_users = set()
            for genre in genres:
                resp = subscriptions_table.query(
                    KeyConditionExpression=Key('contentKey').eq(f"genre#{genre}")
                )
                target_users.update([item['user'] for item in resp.get('Items', [])])

            resp = subscriptions_table.query(
                KeyConditionExpression=Key('contentKey').eq(f"artist#{artist_id}")
            )
            target_users.update([item['user'] for item in resp.get('Items', [])])

            rating_resp = ratings_table.query(
                IndexName=ratings_table_gsi_artist_id,
                KeyConditionExpression=Key('artistId').eq(artist_id),
                ProjectionExpression='#usr',
                ExpressionAttributeNames={'#usr': 'user'},
                Limit = 50,
            )
            target_users.update([r['user'] for r in rating_resp.get('Items', [])])

            history_resp = listening_history_table.query(
                IndexName=listening_history_table_gsi_artist_id,
                KeyConditionExpression=Key('artistId').eq(artist_id),
                ProjectionExpression='#usr',
                ExpressionAttributeNames={'#usr': 'user'},
                Limit = 50,
            )
            target_users.update([h['user'] for h in history_resp.get('Items', [])])

            now = datetime.utcnow()
            with user_feed_table.batch_writer() as batch:
                for user in target_users:
                    score = 0.0

                    # subscription
                    score += 0.5

                    # rating history
                    rating_resp = ratings_table.query(
                        KeyConditionExpression=boto3.dynamodb.conditions.Key('user').eq(user),
                        Limit = 50
                    )
                    for r in rating_resp.get('Items', []):
                        if r['artistId'] == artist_id:
                            rating = float(r.get('rating', 0))
                            if rating == 0:
                                continue
                            score += (rating - 3) / 4

                    # Listening history
                    history_resp = listening_history_table.query(
                        KeyConditionExpression=Key('user').eq(user),
                        Limit=50,
                        ScanIndexForward=False
                    )
                    for h in history_resp.get('Items', []):
                        if set(h.get('genres', [])) & set(genres):
                            #"2023-10-01T12:00:00Z"
                            ts = datetime.fromisoformat(h['timestamp'].replace('Z', '+00:00'))
                            hours_ago = (now - ts).total_seconds() / 3600

                            if hours_ago < 24:
                                score += 0.2
                            elif hours_ago < 168:
                                score += 0.1
                            else:
                                score += 0.05

                            break

                    batch.put_item(
                        Item={
                            "user": user,
                            "timestamp": now.isoformat(),
                            "contentKey": content_key,
                            "score": Decimal(str(score))
                        }
                    )

        return {
            'statusCode': 200,
            'body': json.dumps({'message': f'Feed updated for users'})
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }