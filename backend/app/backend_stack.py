from aws_cdk import (
    Stack,
    aws_dynamodb as dynamodb,
    aws_s3 as s3,
    aws_lambda as _lambda,
    Duration,
    aws_apigateway as apigw,
    aws_cognito as cognito,
    RemovalPolicy,
)
from constructs import Construct
from app.config import AppConfig

class BackendStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        # self.artists_table = dynamodb.Table(
        #     self, "ArtistsTable",
        #     table_name=AppConfig.ARTISTS_TABLE,
        #     partition_key=dynamodb.Attribute(
        #         name="artistId",
        #         type=dynamodb.AttributeType.STRING
        #     ),
        #     removal_policy=RemovalPolicy.DESTROY
        # )
        self.artists_table = dynamodb.Table.from_table_name(self, "ArtistsTable", "Artists")
        # self.genres_table = dynamodb.Table(
        #     self, "GenresTable",
        #     table_name=AppConfig.GENRES_TABLE,
        #     partition_key=dynamodb.Attribute(
        #         name="genreName",
        #         type=dynamodb.AttributeType.STRING
        #     ),
        #     removal_policy=RemovalPolicy.DESTROY
        # )
        self.genres_table = dynamodb.Table.from_table_name(self, "GenresTable", "Genres")
        # self.songs_table = dynamodb.Table(
        #     self, "SongsTable",
        #     table_name=AppConfig.SONGS_TABLE,
        #     partition_key=dynamodb.Attribute(
        #         name="songId",
        #         type=dynamodb.AttributeType.STRING
        #     ),
        #     removal_policy=RemovalPolicy.DESTROY
        # )
        self.songs_table = dynamodb.Table.from_table_name(self, "SongsTable", "Songs")
        # self.albums_table = dynamodb.Table(
        #     self, "AlbumsTable",
        #     table_name=AppConfig.ALBUMS_TABLE,
        #     partition_key=dynamodb.Attribute(
        #         name="albumId",
        #         type=dynamodb.AttributeType.STRING
        #     ),
        #     removal_policy=RemovalPolicy.DESTROY
        # )
        self.albums_table = dynamodb.Table.from_table_name(self, "AlbumsTable", "Albums")

        # self.albums_bucket = s3.Bucket(
        #     self, "AlbumsBucket",
        #     bucket_name=AppConfig.ALBUMS_BUCKET,
        #     removal_policy=RemovalPolicy.DESTROY,
        #     auto_delete_objects=True
        # )
        self.albums_bucket = s3.Bucket.from_bucket_name(self, "AlbumsBucket", "AlbumsBucket1B60D665")
        # self.songs_bucket = s3.Bucket(
        #     self, "SongsBucket",
        #     bucket_name=AppConfig.SONGS_BUCKET,
        #     removal_policy=RemovalPolicy.DESTROY,
        #     auto_delete_objects=True
        # )
        self.songs_bucket = s3.Bucket.from_bucket_name(self, "SongsBucket", "SongsBucketED641A29")

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
                "BUCKET": AppConfig.BUCKET,
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
                "BUCKET": AppConfig.BUCKET,
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
                "BUCKET": AppConfig.BUCKET,
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
                "BUCKET": AppConfig.BUCKET,
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
                "BUCKET": AppConfig.BUCKET,
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
                "BUCKET": AppConfig.BUCKET,
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

        # --- API Gateway ---
        self.api = apigw.RestApi(
            self, "dhox6eq69e",
            rest_api_name="cloud-music-app",
            deploy_options=apigw.StageOptions(stage_name="dev")
        )

        # /albums
        albums = self.api.root.add_resource("albums")
        albums.add_method("POST", apigw.LambdaIntegration(self.create_album_lambda))
        albums.add_method("GET", apigw.LambdaIntegration(self.get_all_albums_lambda))

        # /albums/{id}
        album_by_id = albums.add_resource("{id}")
        album_by_id.add_method("GET", apigw.LambdaIntegration(self.get_album_by_id_lambda))

        # /albums/new10
        new_albums = albums.add_resource("new10")
        new_albums.add_method("GET", apigw.LambdaIntegration(self.get_10_new_albums_lambda))

        # /albums/url
        album_url = albums.add_resource("url")

        # /albums/url/{key}
        album_url_by_key = album_url.add_resource("{key}")
        album_url_by_key.add_method("GET", apigw.LambdaIntegration(self.get_album_track_lambda))

        # /artists
        artists = self.api.root.add_resource("artists")
        artists.add_method("GET", apigw.LambdaIntegration(self.get_all_artists_lambda))
        artists.add_method("POST", apigw.LambdaIntegration(self.create_artist_lambda))

        # /artists/new10
        new_artists = artists.add_resource("new10")
        new_artists.add_method("GET", apigw.LambdaIntegration(self.get_10_new_artists_lambda))

        # /genres
        genres = self.api.root.add_resource("genres")
        genres.add_method("GET", apigw.LambdaIntegration(self.get_all_genres_lambda))

        # /songs
        songs = self.api.root.add_resource("songs")
        songs.add_method("GET", apigw.LambdaIntegration(self.get_all_songs_lambda))
        songs.add_method("POST", apigw.LambdaIntegration(self.create_song_lambda))
        songs.add_method("PUT", apigw.LambdaIntegration(self.edit_song_lambda))

        # /songs/{id}
        song_by_id = songs.add_resource("{id}")
        song_by_id.add_method("GET", apigw.LambdaIntegration(self.get_song_by_id_lambda))
        song_by_id.add_method("DELETE", apigw.LambdaIntegration(self.delete_song_lambda))

        # /songs/url
        song_url = songs.add_resource("url")

        # /songs/url/{fileKey}
        song_url_by_key = song_url.add_resource("{fileKey}")
        song_url_by_key.add_method("GET", apigw.LambdaIntegration(self.get_song_track_lambda))


        # CORS
        # /albums
        albums.add_cors_preflight(
            allow_origins=apigw.Cors.ALL_ORIGINS,
            allow_methods=["GET", "POST", "OPTIONS"]
        )

        # /albums/{id}
        album_by_id.add_cors_preflight(
            allow_origins=apigw.Cors.ALL_ORIGINS,
            allow_methods=["GET", "OPTIONS"]
        )

        # /albums/new10
        new_albums.add_cors_preflight(
            allow_origins=apigw.Cors.ALL_ORIGINS,
            allow_methods=["GET", "OPTIONS"]
        )

        # /albums/url/{key}
        album_url_by_key.add_cors_preflight(
            allow_origins=apigw.Cors.ALL_ORIGINS,
            allow_methods=["GET", "OPTIONS"]
        )

        # /artists
        artists.add_cors_preflight(
            allow_origins=apigw.Cors.ALL_ORIGINS,
            allow_methods=["GET", "POST", "OPTIONS"]
        )

        # /artists/new10
        new_artists.add_cors_preflight(
            allow_origins=apigw.Cors.ALL_ORIGINS,
            allow_methods=["GET", "OPTIONS"]
        )

        # /genres
        genres.add_cors_preflight(
            allow_origins=apigw.Cors.ALL_ORIGINS,
            allow_methods=["GET", "OPTIONS"]
        )

        # /songs
        songs.add_cors_preflight(
            allow_origins=apigw.Cors.ALL_ORIGINS,
            allow_methods=["GET", "POST", "PUT", "OPTIONS"]
        )

        # /songs/{id}
        song_by_id.add_cors_preflight(
            allow_origins=apigw.Cors.ALL_ORIGINS,
            allow_methods=["GET", "DELETE", "OPTIONS"]
        )

        # /songs/url/{fileKey}
        song_url_by_key.add_cors_preflight(
            allow_origins=apigw.Cors.ALL_ORIGINS,
            allow_methods=["GET", "OPTIONS"]
        )


        # --- Cognito User Pool ---
        self.user_pool = cognito.UserPool(
            self, AppConfig.COGNITO_USER_POOL_ID,
            user_pool_name=AppConfig.COGNITO_USER_POOL_NAME,
            self_sign_up_enabled=True,
            sign_in_aliases=cognito.SignInAliases(email=True),
            auto_verify=cognito.AutoVerifiedAttrs(email=True),
            standard_attributes=cognito.StandardAttributes(
                email=cognito.StandardAttribute(required=True, mutable=True)
            ),
            password_policy=cognito.PasswordPolicy(
                min_length=8,
                require_lowercase=True,
                require_uppercase=True,
                require_digits=True,
                require_symbols=False
            ),
            removal_policy=RemovalPolicy.DESTROY
        )

        self.user_pool_client = cognito.UserPoolClient(
            self, id=AppConfig.COGNITO_CLIENT_ID,
            user_pool=self.user_pool,
            generate_secret=False,
            o_auth=cognito.OAuthSettings(
                callback_urls=AppConfig.COGNITO_CLIENT_CALLBACK_URLS,
                logout_urls=AppConfig.COGNITO_CLIENT_LOGOUT_URLS,
                flows=cognito.OAuthFlows(authorization_code_grant=True),
            )
        )

        self.user_group_admins = cognito.CfnUserPoolGroup(
            self,
            id=AppConfig.COGNITO_GROUP_ADMINS_ID,
            group_name=AppConfig.COGNITO_GROUP_ADMINS,
            user_pool_id=self.user_pool.user_pool_id
        )

        self.user_group_auth_users = cognito.CfnUserPoolGroup(
            self,
            id=AppConfig.COGNITO_GROUP_AUTH_USERS_ID,
            group_name=AppConfig.COGNITO_GROUP_AUTH_USERS,
            user_pool_id=self.user_pool.user_pool_id
        )

        self.post_register_lambda = _lambda.Function(
            self, "PostRegisterConfirmationLambda",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="index.lambda_handler",
            code=_lambda.Code.from_asset(AppConfig.POST_REGISTER_LAMBDA),
            timeout=Duration.seconds(10),
            environment={
                "USER_POOL_ID": self.user_pool.user_pool_id,
                "GROUP_NAME": AppConfig.COGNITO_GROUP_AUTH_USERS
            }
        )

        self.user_pool.add_trigger(cognito.UserPoolOperation.POST_CONFIRMATION, self.post_register_lambda)
