class AppConfig:
    REGION = "eu-central-1"

    # DynamoDB
    ARTISTS_TABLE = "Artists"
    GENRES_TABLE = "Genres"
    SONGS_TABLE = "Songs"
    ALBUMS_TABLE = "Albums"

    # S3 buckets
    BUCKET = "music-app-content-dhox6eq69e"
    ALBUMS_BUCKET = "albums"
    SONGS_BUCKET = "songs"

    # Cognito
    COGNITO_CLIENT_LOGOUT_URLS = ["http://localhost:4200/home"]
    COGNITO_CLIENT_CALLBACK_URLS = ["http://localhost:4200/home"]
    COGNITO_USER_POOL_ID = "eu-central-1_vS3vkgRGf"
    COGNITO_USER_POOL_NAME = "User pool - uoahua"
    COGNITO_CLIENT_ID = "cloud-music-app"
    COGNITO_GROUP_ADMINS = "Admins"
    COGNITO_GROUP_ADMINS_ID = "AdminsGroup"
    COGNITO_GROUP_AUTH_USERS = "AuthUsers"
    COGNITO_GROUP_AUTH_USERS_ID = "AuthUsersGroup"

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