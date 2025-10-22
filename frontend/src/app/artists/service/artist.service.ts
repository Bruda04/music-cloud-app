import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { Artist } from '../model/artist.model';
import { environment } from '../../environment/environment';
import {HttpClient, HttpParams} from '@angular/common/http';
import {PaginatedArtists, PaginatedSongs} from '../../songs/model/song.model';

@Injectable({
  providedIn: 'root'
})
export class ArtistService {

  constructor(private httpClient: HttpClient) {}

  createArtist(artist: Artist): Observable<{"message":String,"artist":Artist}> {
    return this.httpClient.post<{"message":String,"artist":Artist}>(`${environment.apiUrl}/artists`,artist);
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

  getAllMock():Artist[]{
    //mock because its on homepage and I want to keep my requests low for now
    return[
      { artistId: '1', name: 'John Doe', bio: 'Singer and songwriter from NY.', genres: ['Pop', 'Rock'] },
      { artistId: '2', name: 'Jane Smith', bio: 'Jazz vocalist with a smooth style.', genres: ['Jazz'] },
      { artistId: '3', name: 'The Rockers', bio: 'Energetic rock band from LA.', genres: ['Rock', 'Alternative'] },
      { artistId: '4', name: 'DJ Electro', bio: 'Electronic music producer and DJ.', genres: ['EDM', 'House'] },
      { artistId: '5', name: 'Soul Sisters', bio: 'R&B duo with heartfelt lyrics.', genres: ['R&B'] },
      { artistId: '6', name: 'Metal Heads', bio: 'Heavy metal band from Sweden.', genres: ['Metal'] },
      { artistId: '7', name: 'John Doe', bio: 'Singer and songwriter from NY.', genres: ['Pop', 'Rock'] },
      { artistId: '8', name: 'Jane Smith', bio: 'Jazz vocalist with a smooth style.', genres: ['Jazz'] },
      { artistId: '9', name: 'The Rockers', bio: 'Energetic rock band from LA.', genres: ['Rock', 'Alternative'] },
      { artistId: '10', name: 'DJ Electro', bio: 'Electronic music producer and DJ.', genres: ['EDM', 'House'] },
      { artistId: '11', name: 'Soul Sisters', bio: 'R&B duo with heartfelt lyrics.', genres: ['R&B'] },
      { artistId: '12', name: 'Metal Heads', bio: 'Heavy metal band from Sweden.', genres: ['Metal'] },
      { artistId: '13', name: 'John Doe', bio: 'Singer and songwriter from NY.', genres: ['Pop', 'Rock'] },
      { artistId: '14', name: 'Jane Smith', bio: 'Jazz vocalist with a smooth style.', genres: ['Jazz'] },
      { artistId: '15', name: 'The Rockers', bio: 'Energetic rock band from LA.', genres: ['Rock', 'Alternative'] },
      { artistId: '16', name: 'DJ Electro', bio: 'Electronic music producer and DJ.', genres: ['EDM', 'House'] },
      { artistId: '17', name: 'Soul Sisters', bio: 'R&B duo with heartfelt lyrics.', genres: ['R&B'] },
      { artistId: '18', name: 'Metal Heads', bio: 'Heavy metal band from Sweden.', genres: ['Metal'] }
    ]
  }

  get10New(): Observable<Artist[]>{
    return this.httpClient.get<Artist[]>(`${environment.apiUrl}/artists/new10`);
  }

  getById(artistId:string): Observable<Artist>{
    return this.httpClient.get<Artist>(`${environment.apiUrl}/artists/${artistId}`);
  }

  getMock():Artist{
    return { artistId: 'b4863ec7-973b-431b-a8fb-b751a7d821f8', name: 'John Doe', bio: 'Singer and songwriter from NY.', genres: ['Pop', 'Rock'] };
  }
}
