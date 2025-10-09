import { Injectable } from '@angular/core';
import { map, Observable } from 'rxjs';
import { environment } from '../../environment/environment';
import { HttpClient, HttpParams } from '@angular/common/http';
import { CreateSongResponse, PaginatedSongs, Song, Url } from '../model/song.model';

@Injectable({providedIn: 'root'})
export class SongService {

  constructor(private httpClient: HttpClient) {}

  create(song: Song): Observable<CreateSongResponse> {
    return this.httpClient.post<CreateSongResponse>(`${environment.apiUrl}/songs`,song);
  }

  getSongs(limit: number = 6, lastKey?: string): Observable<PaginatedSongs> {
    let params = new HttpParams().set('limit', limit.toString());
    if (lastKey) params = params.set('lastKey', lastKey);

    return this.httpClient.get<PaginatedSongs>(`${environment.apiUrl}/songs`, { params });
  }

  getMockSongs():Song[]{
    return [
      { file: "1759885382-Solar_Waves.mp3",
        title: "Solar Waves", 
        songId: "21f3d794-1e02-4bf9-9a4a-5d30c7547c9f",
        genres: ["ambient", "chill"],
        artistIds: ["artist-123"],
        other:{createdAt: "2025-10-08T01:03:03.207124"},
      },
      {songId: "cd67114b-e440-4822-849d-26b956a8b3fc",
        artistIds: ["5"],
        file: "1759886182-Gilmore_Girls_intro.mp3", 
        other:{createdAt: "2025-10-08T01:03:03.207124", "from series": "Gilmore Girls"}, 
        genres: ["pop", "movie music"], 
        title: "Gilmore Girls intro"
      },
       {songId: "cd67114b-e440-4822-849d-26b956a8b3fc",
        artistIds: ["5"],
        file: "1759886182-Gilmore_Girls_intro.mp3", 
        other:{createdAt: "2025-10-08T01:03:03.207124", "from series": "Gilmore Girls"}, 
        genres: ["pop", "movie music"], 
        title: "Gilmore Girls intro"
      },
    ]
  }

  getUrl(fileKey:string):Observable<Url>{
    return this.httpClient.get<Url>(`${environment.apiUrl}/songs/url/${fileKey}`)
  }
}
