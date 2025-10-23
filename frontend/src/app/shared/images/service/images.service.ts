import { Injectable } from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {map, Observable} from 'rxjs';
import {environment} from '../../../environment/environment';

@Injectable({
  providedIn: 'root'
})
export class ImagesService {
  constructor(private httpClient: HttpClient) {
  }
  url: string = '';
  getSongImageUrl(imageFileKey: string): Observable<string> {
    return this.httpClient
      .get<{ url: string; }>(`${environment.apiUrl}/images/songs/${imageFileKey}`)
      .pipe(map(resp => resp.url));
  }

  getAlbumImageUrl(imageFileKey: string): Observable<string> {
    return this.httpClient.get<{ url: string }>(`${environment.apiUrl}/images/albums/${imageFileKey}`).pipe(
      map(resp => resp.url)
    );
  }

}
