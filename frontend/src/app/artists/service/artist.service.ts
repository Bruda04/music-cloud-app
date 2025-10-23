import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { Artist } from '../model/artist.model';
import { environment } from '../../environment/environment';
import {HttpClient, HttpParams} from '@angular/common/http';
import {PaginatedArtists, PaginatedSongs, Song} from '../../songs/model/song.model';
import {Album} from '../../albums/model/album.model';

@Injectable({
  providedIn: 'root'
})
export class ArtistService {

  constructor(private httpClient: HttpClient) {}

  createArtist(artist: Artist): Observable<{"message":String,"artist":Artist}> {
    return this.httpClient.post<{"message":String,"artist":Artist}>(`${environment.apiUrl}/artists`,artist);
  }

  getArtistContent(artistId: string | undefined): Observable<{ albums: Album[]; songs: Song[] }> {
    return this.httpClient.get<{"albums":Album[],"songs":Song[]}>(`${environment.apiUrl}/artists/${artistId}/content`);
  }

  editArtist(artist: Artist): Observable<{"message":String,"artistId":string}> {
    return this.httpClient.put<{"message":String,"artistId":string}>(`${environment.apiUrl}/artists`, artist);
  }

  delete(artistId:string): Observable<{"message":String}> {
    return this.httpClient.delete<{"message":String}>(`${environment.apiUrl}/artists/${artistId}`);
  }

  getAllRegular(): Observable<Artist[]> {
    return this.httpClient.get<Artist[]>(`${environment.apiUrl}/artists`);
  }

  getAll(limit: number = 6, lastKey?: string): Observable<PaginatedArtists> {
    let params = new HttpParams().set('limit', limit.toString());
    if (lastKey) params = params.set('lastKey', lastKey);
    return this.httpClient.get<PaginatedArtists>(`${environment.apiUrl}/artists`, { params });
  }


  getById(artistId:string): Observable<Artist>{
    return this.httpClient.get<Artist>(`${environment.apiUrl}/artists/${artistId}`);
  }

  getMock():Artist{
    return { artistId: 'b4863ec7-973b-431b-a8fb-b751a7d821f8', name: 'John Doe', bio: 'Singer and songwriter from NY.', genres: ['Pop', 'Rock'] };
  }
}
