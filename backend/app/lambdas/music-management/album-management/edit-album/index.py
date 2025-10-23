import base64
import json
import boto3
import uuid
import os
from datetime import datetime
import imghdr

from boto3.dynamodb.conditions import Key

s3 = boto3.client('s3')
BUCKET = os.environ['BUCKET']

dynamodb = boto3.resource('dynamodb', region_name=os.environ["REGION"])
albums_table = dynamodb.Table(os.environ['ALBUMS_TABLE'])
albums_table_gsi_id = os.environ['ALBUMS_TABLE_GSI_ID']
genres_table = dynamodb.Table(os.environ['GENRES_TABLE'])
genre_contents_table = dynamodb.Table(os.environ['GENRE_CONTENTS_TABLE'])
artists_table = dynamodb.Table(os.environ['ARTISTS_TABLE'])

def lambda_handler(event, context):
    try:
        claims = event.get("requestContext", {}).get("authorizer", {}).get("claims", {})
        if not claims.get("cognito:groups") or "Admins" not in claims.get("cognito:groups"):
            return {
                'statusCode': 403,
                'headers': _cors_headers(),
                'body': json.dumps({'message': 'Forbidden: Admins only'})
            }

        body = json.loads(event.get('body', '{}'))

        required_fields = ['title', 'artistId', 'genres', 'tracks', 'details']
        missing = [f for f in required_fields if f not in body]
        if missing:
            return _error(400, f"Missing required fields: {', '.join(missing)}")

        # AlbumId can come from query or body
        album_id = body.get('albumId') or event.get('pathParameters', {}).get('albumId')
        if not album_id:
            return _error(400, 'Missing albumId for update.')

        # Check existing album
        gsi_response = albums_table.query(
            IndexName=albums_table_gsi_id,
            KeyConditionExpression=Key('albumId').eq(album_id)
        )

        if not gsi_response['Items']:
            return {
                "statusCode": 404,
                "body": json.dumps({"message": "Album not found"})
            }

        artist_id = gsi_response['Items'][0]['artistId']
        existing_album = albums_table.get_item(Key={'albumId': album_id, 'artistId': artist_id}).get('Item')

        if not existing_album:
            return _error(404, 'Album not found.')

        # Check artist validity
        artist = artists_table.get_item(Key={'artistId': body['artistId']}).get('Item')
        if not artist or artist.get('isDeleted', False):
            return _error(400, 'Artist does not exist or has been deleted.')

        # -----------------------------
        # Handle image replacement
        # -----------------------------
        safe_title = body['title'].replace(' ', '_')
        timestamp = int(datetime.utcnow().timestamp())
        new_image_key = f"{timestamp}-{safe_title}.png"

        image_key = existing_album.get('imageFile', new_image_key)

        image_upload_url = s3.generate_presigned_url(
            'put_object',
            Params={'Bucket': BUCKET, 'Key': f'images/albums/{image_key}', 'ContentType': 'image/png'},
            ExpiresIn=3600
        )

        updated_tracks = []
        override_track_urls = {}
        new_track_urls = []

        existing_tracks_map = {t['songId']: t for t in existing_album.get('tracks', [])}

        incoming_song_ids = set()
        for idx, track in enumerate(body['tracks']):
            title = track.get('title', '').strip()
            if not title:
                return _error(400, f'Missing title for track at index {idx}')

            existing_track = None
            if track.get('songId'):
                existing_track = existing_tracks_map.get(track['songId'])

            # Kreiraj novi songId ako ne postoji
            song_id = existing_track.get('songId') if existing_track else str(uuid.uuid4())
            incoming_song_ids.add(song_id)

            # File key
            timestamp = int(datetime.utcnow().timestamp())
            safe_title = title.replace(' ', '_')
            file_key = existing_track.get('fileKey') if existing_track else f"{timestamp}-{safe_title}.mp3"

            # Presigned PUT URL
            presigned_url = s3.generate_presigned_url(
                'put_object',
                Params={'Bucket': BUCKET, 'Key': f"albums/{file_key}"},
                ExpiresIn=3600
            )

            # Ako postoji existing_track -> override
            if existing_track:
                override_track_urls[song_id] = presigned_url
            else:
                new_track_urls.append(presigned_url)

            # Keep existing rating info i artist info
            rating_sum = existing_track.get('ratingSum', 0) if existing_track else 0
            rating_count = existing_track.get('ratingCount', 0) if existing_track else 0

            updated_track = {
                'songId': song_id,
                'title': title,
                'fileKey': file_key,
                'artistId': artist_id,
                'otherArtistIds': track.get('otherArtistIds', []),
                'lyrics': existing_track.get('lyrics', '') if existing_track else '',
                'ratingSum': rating_sum,
                'ratingCount': rating_count,
                'genres': [g.strip().lower() for g in body['genres'] if g.strip()]
            }

            updated_tracks.append(updated_track)

        # --- Obrisi trackove koji su uklonjeni ---
        for song_id, existing_track in existing_tracks_map.items():
            if song_id not in incoming_song_ids:
                # Briše se fajl sa S3
                if existing_track.get('fileKey'):
                    s3.delete_object(Bucket=BUCKET, Key=f"albums/{existing_track['fileKey']}")

        # -----------------------------
        # Update genre info
        # -----------------------------
        genres = [g.strip().lower() for g in body['genres'] if g.strip()]
        for genre in genres:
            try:
                genres_table.put_item(
                    Item={'genreName': genre},
                    ConditionExpression='attribute_not_exists(#g)',
                    ExpressionAttributeNames={'#g': 'genreName'}
                )
            except genres_table.meta.client.exceptions.ConditionalCheckFailedException:
                pass

        # remove old genre_content links
        old_genres = existing_album.get('genres', [])
        for old in old_genres:
            genre_contents_table.delete_item(
                Key={
                    'genreName': old,
                    'contentKey': f"album#{existing_album['artistId']}#{album_id}"
                }
            )
        # add new ones
        for genre in genres:
            genre_contents_table.put_item(
                Item={
                    'genreName': genre,
                    'contentKey': f"album#{body['artistId']}#{album_id}"
                }
            )

        # -----------------------------
        # Build updated item
        # -----------------------------
        updated_item = {
            **existing_album,
            'albumId': album_id,
            'title': body['title'],
            'artistId': body['artistId'],
            'genres': genres,
            'tracks': updated_tracks,
            'details': body['details'],
            'imageFile': image_key,
            'updatedAt': datetime.utcnow().isoformat()
        }

        # Merge other fields
        if 'other' in body and isinstance(body['other'], dict):
            for k, v in body['other'].items():
                updated_item[k] = v

        # -----------------------------
        # Save updated album
        # -----------------------------
        albums_table.put_item(Item=updated_item)

        return {
            'statusCode': 200,
            'headers': _cors_headers(),
            'body': json.dumps({
                'message': 'Album updated successfully',
                'albumId': album_id,
                'imageUploadUrl': image_upload_url,
                'trackUploadUrls': new_track_urls,
                'trackOverrideUrls' : override_track_urls
            })
        }

    except Exception as e:
        print("Error:", e)
        return _error(500, f'Failed to update album: {str(e)}')


def _error(status, msg):
    return {
        'statusCode': status,
        'headers': _cors_headers(),
        'body': json.dumps({'message': msg})
    }

def _cors_headers():
    return {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "*",
        "Content-Type": "application/json"
    }