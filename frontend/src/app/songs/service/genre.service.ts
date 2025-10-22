import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { environment } from '../../environment/environment';
import { HttpClient } from '@angular/common/http';
import {Genre, GenreContentResponse} from '../model/genre.model';

@Injectable({
  providedIn: 'root'
})
export class GenreService {

  constructor(private httpClient: HttpClient) {}

  getAll(): Observable<Genre[]> {
    return this.httpClient.get<Genre[]>(`${environment.apiUrl}/genres`);
  }

  getContentByGenre(name: string) {
    return this.httpClient.get<GenreContentResponse>(`${environment.apiUrl}/genres/${name}/content`);
  }
}
