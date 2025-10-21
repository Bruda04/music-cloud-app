import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from '../../environment/environment';
import { HttpClient } from '@angular/common/http';
import {Album, CreateAlbumDTO, CreateAlbumResponse} from '../model/album.model';
import { Url } from '../../songs/model/song.model';

@Injectable({providedIn: 'root'})
export class AlbumService {

  constructor(private httpClient: HttpClient) {}

  create(album: CreateAlbumDTO): Observable<CreateAlbumResponse> {
    return this.httpClient.post<CreateAlbumResponse>(`${environment.apiUrl}/albums`,album);
  }

  getAll():Observable<Album[]>{
    return this.httpClient.get<Album[]>(`${environment.apiUrl}/albums`)
  }

  getAllMock(): Album[]{
    return [
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

}
