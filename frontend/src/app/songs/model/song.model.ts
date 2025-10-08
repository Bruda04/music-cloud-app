export interface Song {
    songId?: string,
    title: string,
    artistIds: string[],
    genres: string[],
    fileContentBase64?:string,
    fileKey?:string,
    other?: Record<string,string>,
}
export interface CreateSongResponse{
  songId:string,
  filekey:string,
  message:string
}

export interface PaginatedSongs {
  songs: Song[];
  lastKey?: string;
}

export interface SongUrl{
  url:string
}