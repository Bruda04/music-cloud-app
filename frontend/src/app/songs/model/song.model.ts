import {Artist} from '../../artists/model/artist.model';
import {Album} from '../../albums/model/album.model';

export interface Song {
    songId?: string,
    title: string,
    artist?: { artistId:string, name:string},
    genres: string[],
    file:string, // when create: this is base64, when load: this is fileKey, when edit: not changed=fileKey, changed=base64
    fileChanged?:boolean, //for edit
    otherArtists?:{ artistId:string, name:string}[],
    other?: Record<string,string>,
    artistId?:string, //for create/edit
    otherArtistIds?:string[] //for create/edit
    imageFile?:string, // when create/edit: base64, when load: fileKey
    fileKey?:string, // when load: fileKey
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

export interface PaginatedArtists {
  artists: Artist[];
  lastKey?: string;
}

export interface PaginatedAlbums {
  albums: Album[];
  lastKey?: string;
}



export interface Url{
  url:string
}
