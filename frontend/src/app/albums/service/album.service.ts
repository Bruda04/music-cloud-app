import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from '../../environment/environment';
import {HttpClient, HttpParams} from '@angular/common/http';
import {Album, CreateAlbumDTO, CreateAlbumResponse} from '../model/album.model';
import {PaginatedAlbums, PaginatedArtists, Url} from '../../songs/model/song.model';

@Injectable({providedIn: 'root'})
export class AlbumService {

  constructor(private httpClient: HttpClient) {}

  create(album: CreateAlbumDTO): Observable<CreateAlbumResponse> {
    return this.httpClient.post<CreateAlbumResponse>(`${environment.apiUrl}/albums`,album);
  }

  rateAlbumSong(songId: string, albumId:string, rating:number): Observable<{"message":string}> {
    return this.httpClient.post<{"message":string}>(`${environment.apiUrl}/rate`,{albumId, rating, songId});
  }

  logPlay(albumId: string, songId:string, artistId: string):Observable<{"message":string}>{
    return this.httpClient.post<{"message":string}>(`${environment.apiUrl}/history`, {songId, artistId, contentType: 'album', albumId});
  }

  getAll(limit: number = 6, lastKey?: string): Observable<PaginatedAlbums> {
    let params = new HttpParams().set('limit', limit.toString());
    if (lastKey) params = params.set('lastKey', lastKey);
    return this.httpClient.get<PaginatedAlbums>(`${environment.apiUrl}/albums`, { params });
  }

  getUrl(fileKey:string):Observable<Url>{
    return this.httpClient.get<Url>(`${environment.apiUrl}/albums/url/${fileKey}`)
  }

  getById(id:string):Observable<Album>{
    return this.httpClient.get<Album>(`${environment.apiUrl}/albums/${id}`)
  }

}
