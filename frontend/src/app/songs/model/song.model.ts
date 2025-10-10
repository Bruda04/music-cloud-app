export interface Song {
    songId?: string,
    title: string,
    artistIds: string[],
    genres: string[],
    file:string, // when create: this is base64, when load: this is fileKey, when edit: not changed=fileKey, changed=base64
    fileChanged?:boolean, //for edit
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

export interface Url{
  url:string
}