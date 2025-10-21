class AppConfig:
    REGION = "eu-central-1"

    # DynamoDB
    ARTISTS_TABLE_NAME = "Artists"
    ARTISTS_TABLE_ID = "ArtistsTable"

    GENRES_TABLE_NAME = "Genres"
    GENRES_TABLE_ID = "GenresTable"

    SONGS_TABLE_NAME = "Songs"
    SONGS_TABLE_ID = "SongsTable"
    SONGS_TABLE_GSI_ID = "SongsIdIndex"

    ALBUMS_TABLE_NAME = "Albums"
    ALBUMS_TABLE_ID = "AlbumsTable"
    ALBUMS_TABLE_GSI_ID = "AlbumsIdIndex"

    GENRE_CONTENT_TABLE_NAME = "GenreContents"
    GENRE_CONTENT_TABLE_ID = "GenreContentsTable"

    RATINGS_TABLE_NAME = "Ratings"
    RATINGS_TABLE_ID = "RatingsTable"

    SUBSCRIPTIONS_TABLE_NAME = "Subscriptions"
    SUBSCRIPTIONS_TABLE_ID = "SubscriptionsTable"
    SUBSCRIPTIONS_TABLE_GSI_ID = "SubscriptionsUserIndex"

    USER_FEED_TABLE_NAME = "UserFeed"
    USER_FEED_TABLE_ID = "UserFeedTable"

    LISTENING_HISTORY_TABLE_NAME = "ListeningHistory"
    LISTENING_HISTORY_TABLE_ID = "ListeningHistoryTable"

    # S3 buckets
    CONTENT_BUCKET_NAME = "cloud-music-app-content"
    CONTENT_BUCKET_ID = "cloud-music-app-content-bucket"

    # Cognito
    COGNITO_CLIENT_LOGOUT_URLS = ["http://localhost:4200/home"]
    COGNITO_CLIENT_CALLBACK_URLS = ["http://localhost:4200/home"]
    COGNITO_USER_POOL_ID = "cloud-music-app-user-pool"
    COGNITO_USER_POOL_NAME = "user-pool-cloud-music-app"
    COGNITO_CLIENT_ID = "cloud-music-app-client"
    COGNITO_CLIENT_NAME = "cloud-music-app-cognito-client"
    COGNITO_GROUP_ADMINS = "Admins"
    COGNITO_GROUP_ADMINS_ID = "AdminsGroup"
    COGNITO_GROUP_AUTH_USERS = "AuthUsers"
    COGNITO_GROUP_AUTH_USERS_ID = "AuthUsersGroup"
    COGNITO_AUTHORIZER_ID = "cloud-music-app-authorizer"
    COGNITO_AUTHORIZER_NAME = "cloud-music-app-authorizer"
    USER_POOL_DOMAIN_PREFIX = "cloudmusicapp"
    USER_POOL_DOMAIN_ID = "CognitoDomain"

    # API Gateway
    API_GW_NAME = "cloud-music-app-api"
    API_GW_ID = "cloud-music-app-api-gateway"
    API_GW_STAGE_DEV_NAME = "dev"
    API_GW_STAGE_DEV_ID = "dev-stage"
    API_DEPLOYMENT_ID = "cloud-music-app-api-deployment"

    # SNS
    SNS_PUBLISHING_CONTENT_TOPIC_NAME = "publishingContentTopic"
    SNS_PUBLISHING_CONTENT_TOPIC_ID = "PublishingContentTopicSNS"

    # SQS
    SQS_NOTIFICATION_QUEUE_NAME = "userNotificationQueue"
    SQS_NOTIFICATION_QUEUE_ID = "userNotificationQueueSQS"

    SQS_UPDATE_USER_FEED_QUEUE_NAME = "updateUserFeedQueue"
    SQS_UPDATE_USER_FEED_QUEUE_ID = "UpdateUserFeedQueueSQS"


    # Lambda function paths
    CREATE_ARTIST_LAMBDA = "app/lambdas/artist-management/create-artist"
    GET_ALL_ARTISTS_LAMBDA = "app/lambdas/artist-management/get-all"
    GET_CONTENT_BY_ARTIST_LAMBDA = "app/lambdas/artist-management/get-content-by-artist"
    DELETE_ARTIST_LAMBDA = "app/lambdas/artist-management/delete-artist"

    GET_ALL_GENRES_LAMBDA = "app/lambdas/genre-management/get-all"
    GET_CONTENT_BY_GENRE_LAMBDA = "app/lambdas/genre-management/get-content-by-genre"

    CREATE_ALBUM_LAMBDA = "app/lambdas/music-management/album-management/create-album"
    GET_ALL_ALBUMS_LAMBDA = "app/lambdas/music-management/album-management/get-all"
    GET_ALBUM_BY_ID_LAMBDA = "app/lambdas/music-management/album-management/get-by-id"
    GET_ALBUM_TRACK_LAMBDA = "app/lambdas/music-management/album-management/get-url"
    DELETE_ALBUM_LAMBDA = "app/lambdas/music-management/album-management/delete-album"

    CREATE_SONG_LAMBDA = "app/lambdas/music-management/song-management/create-song"
    DELETE_SONG_LAMBDA = "app/lambdas/music-management/song-management/delete-song"
    EDIT_SONG_LAMBDA = "app/lambdas/music-management/song-management/edit-song"
    GET_ALL_SONGS_LAMBDA = "app/lambdas/music-management/song-management/get-all"
    GET_SONG_BY_ID_LAMBDA = "app/lambdas/music-management/song-management/get-by-id"
    GET_SONG_TRACK_LAMBDA = "app/lambdas/music-management/song-management/get-url"

    RATE_CONTENT_LAMBDA = "app/lambdas/rating-management/rate-content"

    SUBSCRIBE_CONTENT_LAMBDA = "app/lambdas/subscription-management/subscribe"
    UNSUBSCRIBE_CONTENT_LAMBDA = "app/lambdas/subscription-management/unsubscribe"
    NOTIFY_SUBSCRIBERS_LAMBDA = "app/lambdas/subscription-management/notify-subscribers"
    GET_USER_SUBSCRIPTIONS_LAMBDA = "app/lambdas/subscription-management/get-user-subscriptions"

    UPDATE_USER_FEED_LAMBDA = "app/lambdas/user-feed-management/update-user-feed"
    GET_USER_FEED_LAMBDA = "app/lambdas/user-feed-management/get-user-feed"

    LOG_LISTENING_HISTORY_LAMBDA = "app/lambdas/listening-history/log-listening-history"

    POST_REGISTER_LAMBDA = "app/lambdas/cognito/post-confirmation"
    PRE_SIGNUP_LAMBDA = "app/lambdas/cognito/pre-signup"

    IMAGES_GET_LAMBDA = "app/lambdas/images-management/get-url"

    # SES
    SES_FROM_EMAIL = ""
