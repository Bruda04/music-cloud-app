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

    USER_FEED_TABLE_NAME = "UserFeed"
    USER_FEED_TABLE_ID = "UserFeedTable"

    # S3 buckets
    CONTENT_BUCKET_NAME = "cloud-music-app-content-bucket"
    CONTENT_BUCKET_ID = "Cloud Music App Content"
    ALBUMS_BUCKET_PATH = "/albums/"
    SONGS_BUCKET_PATH = "/songs/"
    IMGS_BUCKET_PATH = "/images/"

    # Cognito
    COGNITO_CLIENT_LOGOUT_URLS = ["http://localhost:4200/home"]
    COGNITO_CLIENT_CALLBACK_URLS = ["http://localhost:4200/home"]
    COGNITO_USER_POOL_ID = "cloud-music-app-user-pool"
    COGNITO_USER_POOL_NAME = "User pool for Cloud Music App"
    COGNITO_CLIENT_ID = "cloud-music-app-client"
    COGNITO_CLIENT_NAME = "Cloud Music App Cognito Client"
    COGNITO_GROUP_ADMINS = "Admins"
    COGNITO_GROUP_ADMINS_ID = "AdminsGroup"
    COGNITO_GROUP_AUTH_USERS = "AuthUsers"
    COGNITO_GROUP_AUTH_USERS_ID = "AuthUsersGroup"

    # API Gateway
    API_GW_NAME = "Cloud Music App API"
    API_GW_ID = "cloud-music-app-api-gateway"
    API_GW_STAGE_DEV = "dev"


    # Lambda function paths
    CREATE_ARTIST_LAMBDA = "app/lambdas/artist-management/create-artist"
    GET_10_NEW_ARTISTS_LAMBDA = "app/lambdas/artist-management/get-10-new-artists"
    GET_ALL_ARTISTS_LAMBDA = "app/lambdas/artist-management/get-all"

    GET_ALL_GENRES_LAMBDA = "app/lambdas/genre-management/get-all"
    
    CREATE_ALBUM_LAMBDA = "app/lambdas/music-management/album-management/create-album"
    GET_10_NEW_ALBUMS_LAMBDA = "app/lambdas/music-management/album-management/get-10-new-albums"
    GET_ALL_ALBUMS_LAMBDA = "app/lambdas/music-management/album-management/get-all"
    GET_ALBUM_BY_ID_LAMBDA = "app/lambdas/music-management/album-management/get-by-id"
    GET_ALBUM_TRACK_LAMBDA = "app/lambdas/music-management/album-management/get-url"
    
    CREATE_SONG_LAMBDA = "app/lambdas/music-management/song-management/create-song"
    DELETE_SONG_LAMBDA = "app/lambdas/music-management/song-management/delete-song"
    EDIT_SONG_LAMBDA = "app/lambdas/music-management/song-management/edit-song"
    GET_ALL_SONGS_LAMBDA = "app/lambdas/music-management/song-management/get-all"
    GET_SONG_BY_ID_LAMBDA = "app/lambdas/music-management/song-management/get-by-id"
    GET_SONG_TRACK_LAMBDA = "app/lambdas/music-management/song-management/get-url"

    POST_REGISTER_LAMBDA = "app/lambdas/cognito/post-confirmation"