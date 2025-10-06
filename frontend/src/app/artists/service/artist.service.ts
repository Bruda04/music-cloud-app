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
  
}
