export interface Album {
    albumId?: string;           
    title: string;              
    artistIds: string[];        
    genres: string[];           
    tracks: TrackDTO[];     
    other?: Record<string,string>;
}

export interface AlbumTrack {
  title: string;
  file?: File;
  fileBase64?: string;
  dragging?: boolean
}

export interface TrackDTO{
    title:string,
    file:string
}

export interface CreateAlbumResponse{
    message: string,
    albumId: string,
    tracks: TrackDTO[]
}
