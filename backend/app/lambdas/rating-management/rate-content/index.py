import json
import os
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb', region_name=os.environ["REGION"])
ratings_table = dynamodb.Table(os.environ["RATINGS_TABLE"])
songs_table = dynamodb.Table(os.environ["SONGS_TABLE"])
songs_table_index = os.environ["SONGS_TABLE_GSI"]
albums_table = dynamodb.Table(os.environ["ALBUMS_TABLE"])
albums_table_index = os.environ["ALBUMS_TABLE_GSI"]

def lambda_handler(event, context):
    try:
        claims = event.get("requestContext", {}).get("authorizer", {}).get("claims", {})
        user = claims.get("email")
        if not user:
            return _response(400, {'error': 'User email not found in token'})

        body = json.loads(event.get('body', '{}'))
        rating = int(body.get('rating', 0))
        song_id = body.get('songId')
        album_id = body.get('albumId')

        if not song_id:
            return _response(400, {'error': 'songId is required'})

        if album_id:
            content_key = f"album#{album_id}#song#{song_id}"
        else:
            content_key = f"song#{song_id}"

        artist_id = None

        if album_id:
            gsi_response = albums_table.query(
                IndexName=albums_table_index,
                KeyConditionExpression=Key('albumId').eq(album_id)
            )

            if not gsi_response.get('Items'):
                return _response(404, {'error': 'Album not found'})

            album_item = gsi_response['Items'][0]
            artist_id = album_item.get('artistId')
            if not artist_id:
                artist_id = "unknown-artist"

            album = albums_table.get_item(Key={'albumId': album_id, 'artistId': artist_id}).get('Item', {})
            if album and 'tracks' in album:
                updated_tracks = []
                for track in album['tracks']:
                    if track.get('songId') == song_id:
                        track['ratingCount'] = track.get('ratingCount', 0) + 1
                        track['ratingSum'] = track.get('ratingSum', 0) + rating
                    updated_tracks.append(track)

                albums_table.update_item(
                    Key={'albumId': album_id, 'artistId': artist_id},
                    UpdateExpression="SET tracks = :tracks",
                    ExpressionAttributeValues={':tracks': updated_tracks}
                )

        else:
            gsi_response = songs_table.query(
                IndexName=songs_table_index,
                KeyConditionExpression=Key('songId').eq(song_id)
            )

            if not gsi_response.get('Items'):
                return _response(404, {'error': 'Song not found'})

            song_item = gsi_response['Items'][0]
            artist_id = song_item.get('artistId', 'unknown-artist')

            songs_table.update_item(
                Key={'songId': song_id, 'artistId': artist_id},
                UpdateExpression="SET ratingCount = if_not_exists(ratingCount, :zero) + :inc, "
                                 "ratingSum = if_not_exists(ratingSum, :zero) + :r",
                ExpressionAttributeValues={
                    ':inc': 1,
                    ':r': rating,
                    ':zero': 0
                },
                ReturnValues="UPDATED_NEW"
            )

        ratings_table.put_item(
            Item={
                'contentKey': content_key,
                'user': user,
                'rating': rating,
                'artistId': artist_id or "unknown-artist"
            }
        )

        return _response(200, {'message': 'Rating added successfully'})

    except Exception as e:
        print("Error:", e)
        return _response(500, {'error': str(e)})


def _response(status_code, body):
    return {
        'statusCode': status_code,
        'headers': {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST",
            "Content-Type": "application/json"
        },
        'body': json.dumps(body)
    }