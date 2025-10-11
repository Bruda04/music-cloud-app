class AppConfig:
    REGION = "eu-central-1"

    ARTISTS_TABLE = "Artists"
    GENRES_TABLE = "Genres"
    SONGS_TABLE = "Songs"
    ALBUMS_TABLE = "Albums"

    # S3 buckets
    ALBUMS_BUCKET = "music-app-content-dhox6eq69e/albums"
    SONGS_BUCKET = "music-app-content-dhox6eq69e/songs"

    CREATE_ARTIST_LAMBDA = "lambdas/artist-management/create-artist"
    GET_10_NEW_ARTISTS_LAMBDA = "lambdas/artist-management/get-10-new-artists"
    GET_ALL_ARTISTS_LAMBDA = "lambdas/artist-management/get-all"

    GET_ALL_GENRES_LAMBDA = "lambdas/genre-management/get-all"
    
    CREATE_ALBUM_LAMBDA = "lambdas/music-management/album-management/create-album"
    GET_10_NEW_ALBUMS_LAMBDA = "lambdas/music-management/album-management/get-10-new-albums"
    GET_ALL_ALBUMS_LAMBDA = "lambdas/music-management/album-management/get-all"
    GET_ALBUM_BY_ID_LAMBDA = "lambdas/music-management/album-management/get-by-id"
    GET_ALBUM_TRACK_LAMBDA = "lambdas/music-management/album-management/get-url"
    
    CREATE_SONG_LAMBDA = "lambdas/music-management/song-management/create-song"
    DELETE_SONG_LAMBDA = "lambdas/music-management/song-management/delete-song"
    EDIT_SONG_LAMBDA = "lambdas/music-management/song-management/edit-song"
    GET_ALL_SONGS_LAMBDA = "lambdas/music-management/song-management/get-all"
    GET_SONG_BY_ID_LAMBDA = "lambdas/music-management/song-management/get-by-id"
    GET_SONG_TRACK_LAMBDA = "lambdas/music-management/song-management/get-url"