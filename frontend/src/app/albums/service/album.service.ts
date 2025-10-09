import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from '../../environment/environment';
import { HttpClient } from '@angular/common/http';
import { Album, CreateAlbumResponse } from '../model/album.model';
import { Url } from '../../songs/model/song.model';

@Injectable({providedIn: 'root'})
export class AlbumService {

  constructor(private httpClient: HttpClient) {}

  create(album: Album): Observable<CreateAlbumResponse> {
    return this.httpClient.post<CreateAlbumResponse>(`${environment.apiUrl}/albums`,album);
  }

  getAll():Observable<Album[]>{
    return this.httpClient.get<Album[]>(`${environment.apiUrl}/albums`)
  }

  getAllMock(): Album[]{
    return [
      {
        albumId:"1",
        title: "Album 1",
        artistIds: ["edd7330b-f5b5-48db-9755-107941db3211", "1"],
        genres: ["rock","pop"],
        tracks: [{title: "track 1",fileKey: "1759958247-track_003.mp3"},{title: "track 2",fileKey: "1759958247-track_003.mp3"}],
      },
      {        
        albumId:"2",
        title: "Album 2",
        artistIds: ["edd7330b-f5b5-48db-9755-107941db3211", "1"],
        genres: ["rock","pop"],
        tracks: [{title: "track 1",fileKey: "1759958247-track_003.mp3"},{title: "track 2",fileKey: "1759958247-track_003.mp3"}],
      },
      {
        albumId:"3",
        title: "Album 3",
        artistIds: ["edd7330b-f5b5-48db-9755-107941db3211", "1"],
        genres: ["rock","pop"],
        tracks: [{title: "track 1",fileKey: "1759958247-track_003.mp3"},{title: "track 2",fileKey: "1759958247-track_003.mp3"}]
      },
      {
        albumId:"4",
        title: "Album 4",
        artistIds: ["edd7330b-f5b5-48db-9755-107941db3211", "1"],
        genres: ["rock","pop"],
        tracks: [{title: "track 1",fileKey: "1759958247-track_003.mp3"},{title: "track 2",fileKey: "1759958247-track_003.mp3"}]
      },
      {
        albumId:"5",
        title: "Album 5",
        artistIds: ["edd7330b-f5b5-48db-9755-107941db3211", "1"],
        genres: ["rock","pop"],
        tracks: [{title: "track 1",fileKey: "1759958247-track_003.mp3"},{title: "track 2",fileKey: "1759958247-track_003.mp3"}]
      },
      {
        albumId:"6",
        title: "Album 6",
        artistIds: ["edd7330b-f5b5-48db-9755-107941db3211", "1"],
        genres: ["rock","pop"],
        tracks: [{title: "track 1",fileKey: "1759958247-track_003.mp3"},{title: "track 2",fileKey: "1759958247-track_003.mp3"}]
      },
    ]
  }

  get10New():Observable<Album[]>{
    return this.httpClient.get<Album[]>(`${environment.apiUrl}/albums/new10`);
  }

  getUrl(fileKey:string):Observable<Url>{
    return this.httpClient.get<Url>(`${environment.apiUrl}/albums/url/${fileKey}`)
  }

  getById(id:string):Observable<Album>{
    return this.httpClient.get<Album>(`${environment.apiUrl}/albums/${id}`)
  }

  getMock():Album{
    return {
      albumId:"1",
      title: "Album 1",
      artistIds: ["edd7330b-f5b5-48db-9755-107941db3211", "1"],
      genres: ["rock","jazz"],
      tracks: [{title: "track 1",fileKey: "1759958247-track_003.mp3"},{title: "track 2",fileKey: "1759958247-track_003.mp3"}],
      other: {
        details:"Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged."
      }
    }
  }
}
