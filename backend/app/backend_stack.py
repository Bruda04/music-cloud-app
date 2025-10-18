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
        self.artists_table = dynamodb.Table(
            self, AppConfig.ARTISTS_TABLE_ID,
            table_name=AppConfig.ARTISTS_TABLE_NAME,
            partition_key=dynamodb.Attribute(
                name="artistId",
                type=dynamodb.AttributeType.STRING
            ),
            removal_policy=RemovalPolicy.DESTROY
        )
        #self.artists_table = dynamodb.Table.from_table_name(self, "ArtistsTable", "Artists")

        self.genres_table = dynamodb.Table(
            self, AppConfig.GENRES_TABLE_ID,
            table_name=AppConfig.GENRES_TABLE_NAME,
            partition_key=dynamodb.Attribute(
                name="genreName",
                type=dynamodb.AttributeType.STRING
            ),
            removal_policy=RemovalPolicy.DESTROY
        )
        # self.genres_table = dynamodb.Table.from_table_name(self, "GenresTable", "Genres")

        self.songs_table = dynamodb.Table(
            self, AppConfig.SONGS_TABLE_ID,
            table_name=AppConfig.SONGS_TABLE_NAME,
            partition_key=dynamodb.Attribute(
                name="artistId",
                type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(
                name="songId",
                type=dynamodb.AttributeType.STRING
            ),
            removal_policy=RemovalPolicy.DESTROY
        )
        self.songs_table.add_global_secondary_index(
            index_name=AppConfig.SONGS_TABLE_GSI_ID,
            partition_key=dynamodb.Attribute(
                name="songId",
                type=dynamodb.AttributeType.STRING
            ),
            projection_type=dynamodb.ProjectionType.KEYS_ONLY
        )
        # self.songs_table = dynamodb.Table.from_table_name(self, "SongsTable", "Songs")

        self.albums_table = dynamodb.Table(
            self, AppConfig.ALBUMS_TABLE_ID,
            table_name=AppConfig.ALBUMS_TABLE_NAME,
            partition_key=dynamodb.Attribute(
                name="artistId",
                type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(
                name="albumId",
                type=dynamodb.AttributeType.STRING
            ),
            removal_policy=RemovalPolicy.DESTROY
        )
        self.albums_table.add_global_secondary_index(
            index_name=AppConfig.ALBUMS_TABLE_GSI_ID,
            partition_key=dynamodb.Attribute(
                name="albumId",
                type=dynamodb.AttributeType.STRING
            ),
            projection_type=dynamodb.ProjectionType.KEYS_ONLY
        )
        # self.albums_table = dynamodb.Table.from_table_name(self, "AlbumsTable", "Albums")

        self.genre_contents_table = dynamodb.Table(
            self, AppConfig.GENRE_CONTENT_TABLE_ID,
            table_name=AppConfig.GENRE_CONTENT_TABLE_NAME,
            partition_key=dynamodb.Attribute(
                name="genreName",
                type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(
                name="contentKey", # <contentType>#<contentId> (e.g., "album#1234", "song#5678")
                type=dynamodb.AttributeType.STRING
            ),
            removal_policy=RemovalPolicy.DESTROY
        )

        self.ratings_table = dynamodb.Table(
            self, AppConfig.RATINGS_TABLE_ID,
            table_name=AppConfig.RATINGS_TABLE_NAME,
            partition_key=dynamodb.Attribute(
                name="user",
                type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(
                name="contentKey", # <contentType>#<contentId> (e.g., "album#1234", "song#5678")
                type=dynamodb.AttributeType.STRING
            ),
            removal_policy=RemovalPolicy.DESTROY
        )

        self.subscriptions_table = dynamodb.Table(
            self, AppConfig.SUBSCRIPTIONS_TABLE_ID,
            table_name=AppConfig.SUBSCRIPTIONS_TABLE_NAME,
            partition_key=dynamodb.Attribute(
                name="contentKey", # <contentType>#<contentId> (e.g., "album#1234", "song#5678")
                type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(
                name="user",
                type=dynamodb.AttributeType.STRING
            ),
            removal_policy=RemovalPolicy.DESTROY
        )

        self.subscriptions_table.add_global_secondary_index(
            index_name=AppConfig.SUBSCRIPTIONS_TABLE_GSI_ID,
            partition_key=dynamodb.Attribute(
                name="user",
                type=dynamodb.AttributeType.STRING
            ),
            projection_type=dynamodb.ProjectionType.KEYS_ONLY
        )

        self.user_feed_table = dynamodb.Table(
            self, AppConfig.USER_FEED_TABLE_ID,
            table_name=AppConfig.USER_FEED_TABLE_NAME,
            partition_key=dynamodb.Attribute(
                name="user",
                type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(
                name="timestamp",
                type=dynamodb.AttributeType.STRING
            ),
            removal_policy=RemovalPolicy.DESTROY
        )

        # --- Cognito User Pool ---
        self.user_pool = cognito.UserPool(
            self, AppConfig.COGNITO_USER_POOL_ID,
            user_pool_name=AppConfig.COGNITO_USER_POOL_NAME,
            self_sign_up_enabled=True,
            sign_in_aliases=cognito.SignInAliases(email=True, username=True),
            auto_verify=cognito.AutoVerifiedAttrs(email=True),
            standard_attributes=cognito.StandardAttributes(
                email=cognito.StandardAttribute(required=True, mutable=True),
                given_name=cognito.StandardAttribute(required=True, mutable=True),
                family_name=cognito.StandardAttribute(required=True, mutable=True),
                birthdate=cognito.StandardAttribute(required=True, mutable=True)
            ),
            password_policy=cognito.PasswordPolicy(
                min_length=8,
                require_lowercase=True,
                require_uppercase=True,
                require_digits=True,
                require_symbols=True
            ),
            account_recovery=cognito.AccountRecovery.EMAIL_ONLY,
            mfa=cognito.Mfa.OFF,
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

        self.cognito_authorizer = apigw.CognitoUserPoolsAuthorizer(
            self, AppConfig.COGNITO_AUTHORIZER_ID,
            authorizer_name=AppConfig.COGNITO_AUTHORIZER_NAME,
            cognito_user_pools=[self.user_pool]
        )

        self.post_register_lambda = _lambda.Function(
            self, "PostRegisterConfirmationLambda",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="index.lambda_handler",
            code=_lambda.Code.from_asset(AppConfig.POST_REGISTER_LAMBDA),
            timeout=Duration.seconds(10),
            environment={
                "GROUP_NAME": AppConfig.COGNITO_GROUP_AUTH_USERS
            }
        )

        self.user_pool.add_trigger(
            cognito.UserPoolOperation.POST_CONFIRMATION,
            self.post_register_lambda
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

        # --- S3 Buckets ---
        self.content_bucket = s3.Bucket(
            self,
            AppConfig.CONTENT_BUCKET_ID,
            bucket_name=AppConfig.CONTENT_BUCKET_NAME,
            versioned=False,
            removal_policy=RemovalPolicy.DESTROY,
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
                "ARTISTS_TABLE": AppConfig.ARTISTS_TABLE_NAME,
                "GENRES_TABLE": AppConfig.GENRES_TABLE_NAME,
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
                "ARTISTS_TABLE": AppConfig.ARTISTS_TABLE_NAME,
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
                "ARTISTS_TABLE": AppConfig.ARTISTS_TABLE_NAME,
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
                "GENRES_TABLE": AppConfig.GENRES_TABLE_NAME,
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
                "ALBUMS_TABLE": AppConfig.ALBUMS_TABLE_NAME,
                "GENRES_TABLE": AppConfig.GENRES_TABLE_NAME,
                "BUCKET": AppConfig.CONTENT_BUCKET_NAME,
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
                "ALBUMS_TABLE": AppConfig.ALBUMS_TABLE_NAME,
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
                "ALBUMS_TABLE": AppConfig.ALBUMS_TABLE_NAME,
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
                "ALBUMS_TABLE": AppConfig.ALBUMS_TABLE_NAME,
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
                "BUCKET": AppConfig.CONTENT_BUCKET_NAME,
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
                "BUCKET": AppConfig.CONTENT_BUCKET_NAME,
                "SONGS_TABLE": AppConfig.SONGS_TABLE_NAME,
                "GENRES_TABLE": AppConfig.GENRES_TABLE_NAME,
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
                "BUCKET": AppConfig.CONTENT_BUCKET_NAME,
                "SONGS_TABLE": AppConfig.SONGS_TABLE_NAME,
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
                "BUCKET": AppConfig.CONTENT_BUCKET_NAME,
                "SONGS_TABLE": AppConfig.SONGS_TABLE_NAME,
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
                "SONGS_TABLE": AppConfig.SONGS_TABLE_NAME,
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
                "SONGS_TABLE": AppConfig.SONGS_TABLE_NAME,
                "SONG_TABLE_GSI_ID": AppConfig.SONGS_TABLE_GSI_ID,
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
                "BUCKET": AppConfig.CONTENT_BUCKET_NAME,
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
        self.content_bucket.grant_read_write(self.create_album_lambda)
        self.content_bucket.grant_read(self.get_album_track_lambda)

        # Song lambdas
        self.songs_table.grant_read_write_data(self.create_song_lambda)
        self.songs_table.grant_read_write_data(self.edit_song_lambda)
        self.songs_table.grant_read_write_data(self.delete_song_lambda)
        self.songs_table.grant_read_data(self.get_all_songs_lambda)
        self.songs_table.grant_read_data(self.get_song_by_id_lambda)
        self.content_bucket.grant_read_write(self.create_song_lambda)
        self.content_bucket.grant_read_write(self.edit_song_lambda)
        self.content_bucket.grant_read_write(self.delete_song_lambda)
        self.content_bucket.grant_read(self.get_song_track_lambda)

        self.api = apigw.RestApi(
            self, AppConfig.API_GW_ID,
            rest_api_name=AppConfig.API_GW_NAME,
            deploy=False
        )

        # /albums
        albums = self.api.root.add_resource("albums")
        albums.add_method(
            "POST",
            apigw.LambdaIntegration(self.create_album_lambda),
            authorizer=self.cognito_authorizer,
            authorization_type=apigw.AuthorizationType.COGNITO
        )
        albums.add_method(
            "GET",
            apigw.LambdaIntegration(self.get_all_albums_lambda),
            authorizer=self.cognito_authorizer,
            authorization_type=apigw.AuthorizationType.COGNITO
        )

        # /albums/{id}
        album_by_id = albums.add_resource("{id}")
        album_by_id.add_method(
            "GET",
            apigw.LambdaIntegration(self.get_album_by_id_lambda),
            authorizer=self.cognito_authorizer,
            authorization_type=apigw.AuthorizationType.COGNITO
        )

        # /albums/new10
        new_albums = albums.add_resource("new10")
        new_albums.add_method(
            "GET",
            apigw.LambdaIntegration(self.get_10_new_albums_lambda),
            authorizer=self.cognito_authorizer,
            authorization_type=apigw.AuthorizationType.COGNITO
        )

        # /albums/url
        album_url = albums.add_resource("url")

        # /albums/url/{key}
        album_url_by_key = album_url.add_resource("{key}")
        album_url_by_key.add_method(
            "GET",
            apigw.LambdaIntegration(self.get_album_track_lambda),
            authorizer=self.cognito_authorizer,
            authorization_type=apigw.AuthorizationType.COGNITO
        )

        # /artists
        artists = self.api.root.add_resource("artists")
        artists.add_method(
            "GET",
            apigw.LambdaIntegration(self.get_all_artists_lambda),
            authorizer=self.cognito_authorizer,
            authorization_type=apigw.AuthorizationType.COGNITO
        )
        artists.add_method(
            "POST",
            apigw.LambdaIntegration(self.create_artist_lambda),
            authorizer=self.cognito_authorizer,
            authorization_type=apigw.AuthorizationType.COGNITO
        )

        # /artists/new10
        new_artists = artists.add_resource("new10")
        new_artists.add_method(
            "GET",
            apigw.LambdaIntegration(self.get_10_new_artists_lambda),
            authorizer=self.cognito_authorizer,
            authorization_type=apigw.AuthorizationType.COGNITO
        )

        # /genres
        genres = self.api.root.add_resource("genres")
        genres.add_method(
            "GET",
            apigw.LambdaIntegration(self.get_all_genres_lambda),
            authorizer=self.cognito_authorizer,
            authorization_type=apigw.AuthorizationType.COGNITO
        )

        # /songs
        songs = self.api.root.add_resource("songs")
        songs.add_method(
            "GET",
            apigw.LambdaIntegration(self.get_all_songs_lambda),
            authorizer=self.cognito_authorizer,
            authorization_type=apigw.AuthorizationType.COGNITO
        )
        songs.add_method(
            "POST",
            apigw.LambdaIntegration(self.create_song_lambda),
            authorizer=self.cognito_authorizer,
            authorization_type=apigw.AuthorizationType.COGNITO
        )
        songs.add_method(
            "PUT",
            apigw.LambdaIntegration(self.edit_song_lambda),
            authorizer = self.cognito_authorizer,
            authorization_type = apigw.AuthorizationType.COGNITO
        )

        # /songs/{id}
        song_by_id = songs.add_resource("{id}")
        song_by_id.add_method(
            "GET",
            apigw.LambdaIntegration(self.get_song_by_id_lambda),
            authorizer=self.cognito_authorizer,
            authorization_type=apigw.AuthorizationType.COGNITO
        )
        song_by_id.add_method(
            "DELETE",
            apigw.LambdaIntegration(self.delete_song_lambda),
            authorizer=self.cognito_authorizer,
            authorization_type=apigw.AuthorizationType.COGNITO
        )

        # /songs/url
        song_url = songs.add_resource("url")

        # /songs/url/{fileKey}
        song_url_by_key = song_url.add_resource("{fileKey}")
        song_url_by_key.add_method(
            "GET",
            apigw.LambdaIntegration(self.get_song_track_lambda),
            authorizer=self.cognito_authorizer,
            authorization_type=apigw.AuthorizationType.COGNITO
        )


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

        self.deployment = apigw.Deployment(
            self, AppConfig.API_DEPLOYMENT_ID,
            api=self.api,
            retain_deployments=False
        )

        self.stage = apigw.Stage(
            self, AppConfig.API_GW_STAGE_DEV_ID,
            deployment=self.deployment,
            stage_name=AppConfig.API_GW_STAGE_DEV_NAME)