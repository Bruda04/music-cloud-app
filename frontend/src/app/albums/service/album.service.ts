import { Injectable } from '@angular/core';
import { map, Observable } from 'rxjs';
import { environment } from '../../environment/environment';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Album, CreateAlbumResponse } from '../model/album.model';

@Injectable({providedIn: 'root'})
export class AlbumService {

  constructor(private httpClient: HttpClient) {}

  create(album: Album): Observable<CreateAlbumResponse> {
    return this.httpClient.post<CreateAlbumResponse>(`${environment.apiUrl}/albums`,album);
  }

  getAll():Observable<Album[]>{
    return this.httpClient.get<Album[]>(`${environment.apiUrl}/albums`)
  }

  getMock(): Album[]{
    return [
      {
        title: "Album 1",
        artistIds: ["edd7330b-f5b5-48db-9755-107941db3211", "1"],
        genres: ["rock","pop"],
        tracks: [{title: "track 1",file: "1759958246-track_001.mp3"},{title: "track 2",file: "1759958247-track_002.mp3"}]
      },
      {
        title: "Album 2",
        artistIds: ["edd7330b-f5b5-48db-9755-107941db3211", "1"],
        genres: ["rock","pop"],
        tracks: [{title: "track 1",file: "1759958246-track_001.mp3"},{title: "track 2",file: "1759958247-track_002.mp3"}]
      },
      {
        title: "Album 3",
        artistIds: ["edd7330b-f5b5-48db-9755-107941db3211", "1"],
        genres: ["rock","pop"],
        tracks: [{title: "track 1",file: "1759958246-track_001.mp3"},{title: "track 2",file: "1759958247-track_002.mp3"}]
      },
      {
        title: "Album 4",
        artistIds: ["edd7330b-f5b5-48db-9755-107941db3211", "1"],
        genres: ["rock","pop"],
        tracks: [{title: "track 1",file: "1759958246-track_001.mp3"},{title: "track 2",file: "1759958247-track_002.mp3"}]
      },
      {
        title: "Album 5",
        artistIds: ["edd7330b-f5b5-48db-9755-107941db3211", "1"],
        genres: ["rock","pop"],
        tracks: [{title: "track 1",file: "1759958246-track_001.mp3"},{title: "track 2",file: "1759958247-track_002.mp3"}]
      },
      {
        title: "Album 6",
        artistIds: ["edd7330b-f5b5-48db-9755-107941db3211", "1"],
        genres: ["rock","pop"],
        tracks: [{title: "track 1",file: "1759958246-track_001.mp3"},{title: "track 2",file: "1759958247-track_002.mp3"}]
      },
    ]
  }

  get10New():Observable<Album[]>{
    return this.httpClient.get<Album[]>(`${environment.apiUrl}/albums/new10`);
  }
}
