import { Injectable } from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {environment} from '../../environment/environment';
import {FeedResponseModel} from '../model/feedResponseModel';
import {Observable} from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class FeedService {

  constructor(private httpClient: HttpClient) {
  }

  getFeed(): Observable<FeedResponseModel> {
    return this.httpClient.get<FeedResponseModel>(`${environment.apiUrl}/feed`);
  }

}
