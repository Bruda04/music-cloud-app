import base64
import json
import boto3
import uuid
import os
from datetime import datetime
import imghdr


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
        existing_album = albums_table.get_item(Key={'albumId': album_id}).get('Item')
        if not existing_album:
            return _error(404, 'Album not found.')

        # Check artist validity
        artist = artists_table.get_item(Key={'artistId': body['artistId']}).get('Item')
        if not artist or artist.get('isDeleted', False):
            return _error(400, 'Artist does not exist or has been deleted.')

        # -----------------------------
        # Handle image replacement
        # -----------------------------
        image_key = existing_album.get('imageFile', '')
        if body.get('imageFile'):
            image_bytes = base64.b64decode(body['imageFile'])
            image_type = imghdr.what(None, h=image_bytes)
            if image_type not in ['jpeg', 'png']:
                return _error(400, 'Only JPG and PNG images are supported.')
            ext = 'jpg' if image_type == 'jpeg' else 'png'
            safe_title = body['title'].replace(' ', '_')
            timestamp = int(datetime.utcnow().timestamp())
            new_image_key = f"{timestamp}-{safe_title}.{ext}"

            s3.put_object(
                Bucket=BUCKET,
                Key=f"images/albums/{new_image_key}",
                Body=image_bytes,
                ContentType=f'image/{ext}'
            )
            image_key = new_image_key  # replace

        # -----------------------------
        # Handle tracks
        # -----------------------------
        updated_tracks = []
        for idx, track in enumerate(body['tracks']):
            title = track.get('title', '').strip()
            if not title:
                return _error(400, f'Missing title for track at index {idx}')

            # If a new file is provided, upload and replace fileKey
            file_key = None
            if track.get('file'):
                file_bytes = base64.b64decode(track['file'])
                timestamp = int(datetime.utcnow().timestamp())
                safe_title = title.replace(' ', '_')
                key = f"{timestamp}-{safe_title}.mp3"
                s3.put_object(
                    Bucket=BUCKET,
                    Key=f"albums/{key}",
                    Body=file_bytes,
                    ContentType='audio/mpeg'
                )
                file_key = key
            else:
                # try to reuse from existing album if same title
                existing_track = next(
                    (t for t in existing_album.get('tracks', []) if t.get('title') == title),
                    None
                )
                file_key = existing_track['fileKey'] if existing_track else None

            # Keep existing IDs and rating info if available
            song_id = existing_track.get('songId') if existing_track else str(uuid.uuid4())
            rating_sum = existing_track.get('ratingSum', 0) if existing_track else 0
            rating_count = existing_track.get('ratingCount', 0) if existing_track else 0
            artist_id = existing_track.get('artistId') if existing_track else body['artistId']

            updated_tracks.append({
                'songId': song_id,
                'title': title,
                'fileKey': file_key,
                'artistId': artist_id,
                'otherArtistIds': track.get('otherArtistIds', []),
                'lyrics': existing_track.get('lyrics', '') if existing_track else '',
                'ratingSum': rating_sum,
                'ratingCount': rating_count,
                'genres': [g.strip().lower() for g in body['genres'] if g.strip()]
            })

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
                'albumId': album_id
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