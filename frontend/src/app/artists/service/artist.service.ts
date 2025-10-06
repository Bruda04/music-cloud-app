import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { Artist } from '../model/artist.model';
import { environment } from '../../environment/environment';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class ArtistService {

  constructor(private httpClient: HttpClient) {}

  createArtist(artist: Artist): Observable<{"message":String,"artist":Artist}> {
    return this.httpClient.post<{"message":String,"artist":Artist}>(`${environment.apiUrl}/artists`,artist);
  }

  getAll(): Artist[]{
    //mock for now because its on homepage and i want to keep my requests low for now
    return[
      { artistId: '1', name: 'John Doe', bio: 'Singer and songwriter from NY.', genres: ['Pop', 'Rock'] },
      { artistId: '2', name: 'Jane Smith', bio: 'Jazz vocalist with a smooth style.', genres: ['Jazz'] },
      { artistId: '3', name: 'The Rockers', bio: 'Energetic rock band from LA.', genres: ['Rock', 'Alternative'] },
      { artistId: '4', name: 'DJ Electro', bio: 'Electronic music producer and DJ.', genres: ['EDM', 'House'] },
      { artistId: '5', name: 'Soul Sisters', bio: 'R&B duo with heartfelt lyrics.', genres: ['R&B'] },
      { artistId: '6', name: 'Metal Heads', bio: 'Heavy metal band from Sweden.', genres: ['Metal'] },
      { artistId: '1', name: 'John Doe', bio: 'Singer and songwriter from NY.', genres: ['Pop', 'Rock'] },
      { artistId: '2', name: 'Jane Smith', bio: 'Jazz vocalist with a smooth style.', genres: ['Jazz'] },
      { artistId: '3', name: 'The Rockers', bio: 'Energetic rock band from LA.', genres: ['Rock', 'Alternative'] },
      { artistId: '4', name: 'DJ Electro', bio: 'Electronic music producer and DJ.', genres: ['EDM', 'House'] },
      { artistId: '5', name: 'Soul Sisters', bio: 'R&B duo with heartfelt lyrics.', genres: ['R&B'] },
      { artistId: '6', name: 'Metal Heads', bio: 'Heavy metal band from Sweden.', genres: ['Metal'] },
      { artistId: '1', name: 'John Doe', bio: 'Singer and songwriter from NY.', genres: ['Pop', 'Rock'] },
      { artistId: '2', name: 'Jane Smith', bio: 'Jazz vocalist with a smooth style.', genres: ['Jazz'] },
      { artistId: '3', name: 'The Rockers', bio: 'Energetic rock band from LA.', genres: ['Rock', 'Alternative'] },
      { artistId: '4', name: 'DJ Electro', bio: 'Electronic music producer and DJ.', genres: ['EDM', 'House'] },
      { artistId: '5', name: 'Soul Sisters', bio: 'R&B duo with heartfelt lyrics.', genres: ['R&B'] },
      { artistId: '6', name: 'Metal Heads', bio: 'Heavy metal band from Sweden.', genres: ['Metal'] }
    ]
  }
  
}
