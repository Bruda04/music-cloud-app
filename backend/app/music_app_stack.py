from aws_cdk import (
    Stack,
    aws_dynamodb as dynamodb,
    aws_s3 as s3,
    aws_lambda as _lambda,
    Duration
)
from constructs import Construct
from config import AppConfig

class MusicAppStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.artists_table = dynamodb.Table(
            self, "ArtistsTable",
            table_name=AppConfig.ARTISTS_TABLE,
            partition_key=dynamodb.Attribute(
                name="artistId",
                type=dynamodb.AttributeType.STRING
            ),
            removal_policy=dynamodb.RemovalPolicy.DESTROY
        )

        self.genres_table = dynamodb.Table(
            self, "GenresTable",
            table_name=AppConfig.GENRES_TABLE,
            partition_key=dynamodb.Attribute(
                name="genreName",
                type=dynamodb.AttributeType.STRING
            ),
            removal_policy=dynamodb.RemovalPolicy.DESTROY
        )

        self.songs_table = dynamodb.Table(
            self, "SongsTable",
            table_name=AppConfig.SONGS_TABLE,
            partition_key=dynamodb.Attribute(
                name="songId",
                type=dynamodb.AttributeType.STRING
            ),
            removal_policy=dynamodb.RemovalPolicy.DESTROY
        )

        self.albums_table = dynamodb.Table(
            self, "AlbumsTable",
            table_name=AppConfig.ALBUMS_TABLE,
            partition_key=dynamodb.Attribute(
                name="albumId",
                type=dynamodb.AttributeType.STRING
            ),
            removal_policy=dynamodb.RemovalPolicy.DESTROY
        )

        
        self.albums_bucket = s3.Bucket(
            self, "AlbumsBucket",
            bucket_name=AppConfig.ALBUMS_BUCKET,
            removal_policy=s3.RemovalPolicy.DESTROY,
            auto_delete_objects=True
        )

        self.songs_bucket = s3.Bucket(
            self, "SongsBucket",
            bucket_name=AppConfig.SONGS_BUCKET,
            removal_policy=s3.RemovalPolicy.DESTROY,
            auto_delete_objects=True
        )

        # --- Lambdas ---
        self.create_artist_lambda = _lambda.Function(
            self, "CreateArtistLambda",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="index.lambda_handler",
            code=_lambda.Code.from_asset(AppConfig.CREATE_ARTIST_LAMBDA),
            timeout=Duration.seconds(10),
            environment={
                "ARTISTS_TABLE": AppConfig.ARTISTS_TABLE,
                "GENRES_TABLE": AppConfig.GENRES_TABLE,
                "REGION": AppConfig.REGION
            }
        )
        
        self.get_10_new_artists_lambda = _lambda.Function(
            self, "Get10NewArtistsLambda",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="index.lambda_handler",
            code=_lambda.Code.from_asset(AppConfig.GET_10_NEW_ARTISTS_LAMBDA),
            timeout=Duration.seconds(10),
            environment={
                "ARTISTS_TABLE": AppConfig.ARTISTS_TABLE,
                "REGION": AppConfig.REGION
            }
        )
        
        self.get_all_artists_lambda = _lambda.Function(
            self, "GetAllArtistsLambda",  
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="index.lambda_handler", 
            code=_lambda.Code.from_asset(AppConfig.GET_ALL_ARTISTS_LAMBDA),
            timeout=Duration.seconds(10),
            environment={
                "ARTISTS_TABLE": AppConfig.ARTISTS_TABLE,
                "REGION": AppConfig.REGION
            }
        )

        self.get_all_genres_lambda = _lambda.Function(
            self,"GetAllGenresLambda",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="index.lambda_handler",
            code=_lambda.Code.from_asset(AppConfig.GET_ALL_GENRES_LAMBDA),
            timeout=Duration.seconds(10),
            environment={
                "GENRES_TABLE": AppConfig.GENRES_TABLE,
                "REGION": AppConfig.REGION
            }
        )

        self.create_album_lambda = _lambda.Function(
            self,"CreateAlbumLambda",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="index.lambda_handler",  
            code=_lambda.Code.from_asset(AppConfig.CREATE_ALBUM_LAMBDA),
            timeout=Duration.seconds(20),
            environment={
                "ALBUMS_TABLE": AppConfig.ALBUMS_TABLE,
                "GENRES_TABLE": AppConfig.GENRES_TABLE,
                "BUCKET": "music-app-content-dhox6eq69e",
                "REGION": AppConfig.REGION
            }
        )
        
        self.get_10_new_albums_lambda = _lambda.Function(
            self,"Get10NewAlbumsLambda",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="index.lambda_handler",
            code=_lambda.Code.from_asset(AppConfig.GET_10_NEW_ALBUMS_LAMBDA),
            timeout=Duration.seconds(10),
            environment={
                "ALBUMS_TABLE": AppConfig.ALBUMS_TABLE,
                "REGION": AppConfig.REGION
            }
        )

        self.get_all_albums_lambda = _lambda.Function(
            self,"GetAllAlbumsLambda",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="index.lambda_handler", 
            code=_lambda.Code.from_asset(AppConfig.GET_ALL_ALBUMS_LAMBDA),
            timeout=Duration.seconds(10),
            environment={
                "ALBUMS_TABLE": AppConfig.ALBUMS_TABLE,
                "REGION": AppConfig.REGION
            }
        )

        self.get_album_by_id_lambda = _lambda.Function(
            self,"GetAlbumByIdLambda",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="index.lambda_handler",
            code=_lambda.Code.from_asset(AppConfig.GET_ALBUM_BY_ID_LAMBDA),
            timeout=Duration.seconds(10),
            environment={
                "ALBUMS_TABLE": AppConfig.ALBUMS_TABLE,
                "REGION": AppConfig.REGION
            }
        )

        self.get_album_track_lambda = _lambda.Function(
            self, "GetAlbumTrackLambda",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="index.lambda_handler", 
            code=_lambda.Code.from_asset(AppConfig.GET_ALBUM_TRACK_LAMBDA),
            timeout=Duration.seconds(10),
            environment={
                "BUCKET": "music-app-content-dhox6eq69e",
                "REGION": AppConfig.REGION
            }
        )

        self.create_song_lambda = _lambda.Function(
            self,"CreateSongLambda",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="index.lambda_handler", 
            code=_lambda.Code.from_asset(AppConfig.CREATE_SONG_LAMBDA),
            timeout=Duration.seconds(25),  # upload of files can take a little longer
            environment={
                "BUCKET": "music-app-content-dhox6eq69e",
                "SONGS_TABLE": AppConfig.SONGS_TABLE,
                "GENRES_TABLE": AppConfig.GENRES_TABLE,
                "REGION": AppConfig.REGION
            }
        )

        self.delete_song_lambda = _lambda.Function(
            self,"DeleteSongLambda",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="index.lambda_handler",
            code=_lambda.Code.from_asset(AppConfig.DELETE_SONG_LAMBDA),
            timeout=Duration.seconds(10),
            environment={
                "BUCKET": "music-app-content-dhox6eq69e",
                "SONGS_TABLE": AppConfig.SONGS_TABLE,
                "REGION": AppConfig.REGION
            }
        )

        self.edit_song_lambda = _lambda.Function(
            self, "EditSongLambda",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="index.lambda_handler", 
            code=_lambda.Code.from_asset(AppConfig.EDIT_SONG_LAMBDA),
            timeout=Duration.seconds(10),
            environment={
                "BUCKET": "music-app-content-dhox6eq69e",
                "SONGS_TABLE": AppConfig.SONGS_TABLE,
                "REGION": AppConfig.REGION
            }
        )

        self.get_all_songs_lambda = _lambda.Function(
            self, "GetAllSongsLambda",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="index.lambda_handler",
            code=_lambda.Code.from_asset(AppConfig.GET_ALL_SONGS_LAMBDA),
            timeout=Duration.seconds(10),
            environment={
                "SONGS_TABLE": AppConfig.SONGS_TABLE,
                "REGION": AppConfig.REGION
            }
        )

        self.get_song_by_id_lambda = _lambda.Function(
            self, "GetSongByIdLambda",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="index.lambda_handler", 
            code=_lambda.Code.from_asset(AppConfig.GET_SONG_BY_ID_LAMBDA),
            timeout=Duration.seconds(10),
            environment={
                "SONGS_TABLE": AppConfig.SONGS_TABLE,
                "REGION": AppConfig.REGION
            }
        )

        self.get_song_track_lambda = _lambda.Function(
            self, "GetSongTrackLambda",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="index.lambda_handler",
            code=_lambda.Code.from_asset(AppConfig.GET_SONG_TRACK_LAMBDA),
            timeout=Duration.seconds(10),
            environment={
                "BUCKET": "music-app-content-dhox6eq69e",
                "REGION": AppConfig.REGION
            }
        )

        # --- Grant permissions ---
        # Artist lambdas
        self.artists_table.grant_read_write_data(self.create_artist_lambda)
        self.artists_table.grant_read_data(self.get_all_artists_lambda)
        self.artists_table.grant_read_data(self.get_10_new_artists_lambda)

        # Genre lambda
        self.genres_table.grant_read_data(self.get_all_genres_lambda)
        self.genres_table.grant_read_write_data(self.create_artist_lambda)
        self.genres_table.grant_read_write_data(self.create_song_lambda)
        self.genres_table.grant_read_write_data(self.create_album_lambda)

        # Album lambdas
        self.albums_table.grant_read_write_data(self.create_album_lambda)
        self.albums_table.grant_read_data(self.get_10_new_albums_lambda)
        self.albums_table.grant_read_data(self.get_all_albums_lambda)
        self.albums_table.grant_read_data(self.get_album_by_id_lambda)
        self.albums_bucket.grant_read_write(self.create_album_lambda)
        self.albums_bucket.grant_read(self.get_album_track_lambda)

        # Song lambdas
        self.songs_table.grant_read_write_data(self.create_song_lambda)
        self.songs_table.grant_read_write_data(self.edit_song_lambda)
        self.songs_table.grant_read_write_data(self.delete_song_lambda)
        self.songs_table.grant_read_data(self.get_all_songs_lambda)
        self.songs_table.grant_read_data(self.get_song_by_id_lambda)
        self.songs_bucket.grant_read_write(self.create_song_lambda)
        self.songs_bucket.grant_read_write(self.edit_song_lambda)
        self.songs_bucket.grant_read_write(self.delete_song_lambda)
        self.songs_bucket.grant_read(self.get_song_track_lambda)

