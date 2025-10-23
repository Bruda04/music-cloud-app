import {Artist} from '../../artists/model/artist.model';

export interface Album {
  albumId?: string;
  artist?: Artist;
  title: string;
  artistId: string;           // main artist ID
  genres: string[];
  details: string;
  lyrics?: string;
  imageFile: string;
  createdAt?: string;
  tracks: TrackDTO[];
  other?: Record<string, string>;
}

export interface CreateAlbumDTO {
  title: string;
  artistId: string;           // main artist ID
  genres: string[];
  details: string;
  imageFile?: string;
  tracks?: CreateTrackDTO[];
  other?: Record<string, string>;
  albumId?: string;
}


export interface AlbumTrack {
  title: string;
  file?: File;
  fileBase64?: string;
  dragging?: boolean;
  otherArtistIds?: string[];
}

export interface TrackDTO {
  songId: string;
  otherArtists: Artist[];
  title: string;
  fileKey: string;
  artistId: string;
  otherArtistIds: string[];
  genres: string[];
  ratingSum: number;
  ratingCount: number;
  lyrics: string;
}

export interface CreateTrackDTO {
  title: string;
  file?: string;
  artistId?: string;
  otherArtistIds?: string[];
  genres?: string[];
  lyrics?: string;
}



export interface CreateAlbumResponse{
    message: string,
    albumId: string,
    tracks: TrackDTO[]
}
