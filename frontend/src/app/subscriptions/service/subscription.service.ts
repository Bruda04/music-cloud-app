import { Injectable } from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {environment} from '../../environment/environment';
import {SubscriptionResponse} from '../model/subscriptions.model';
import {Observable} from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class SubscriptionService {
  constructor(private httpClient: HttpClient) {}

  subscribeToArtist(artistId: string){
    return this.subscribe('artist', artistId);
  }

  unsubscribeFromArtist(artistId: string){
    return this.unsubscribe('artist', artistId);
  }

  subscribeToGenre(genreName: string){
    return this.subscribe('genre', genreName);
  }

  unsubscribeFromGenre(genreName: string){
    return this.unsubscribe('genre', genreName);
  }

  getMySubscriptions(): Observable<SubscriptionResponse>{
    return this.httpClient.get<SubscriptionResponse>(`${environment.apiUrl}/subscriptions`);
  }

  private subscribe(contentType: string, contentId: string) {
    return this.httpClient.post(`${environment.apiUrl}/subscribe`, {
      contentType,
      contentId
    });
  }

  private unsubscribe(contentType: string, contentId: string){
    return this.httpClient.delete(`${environment.apiUrl}/unsubscribe`, {
      body: {
        contentType,
        contentId
      }
    });
  }
}
