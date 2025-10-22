import {Component, OnInit} from '@angular/core';
import {FeedService} from './service/feed.service';
import {FeedResponseModel} from './model/feedResponseModel';
import {AsyncPipe, DecimalPipe, NgForOf, NgIf} from '@angular/common';
import {ImagesService} from '../shared/images/service/images.service';
import {catchError, forkJoin, map, of} from 'rxjs';
import {SongsModule} from '../songs/songs.module';
import {Router} from '@angular/router';

@Component({
  selector: 'app-feed',
  templateUrl: './feed.component.html',
  standalone: true,
  styleUrls: ['./feed.component.css', '../shared/themes/card.css', "../shared/themes/all-items.css"],
  imports: [
    NgForOf,
    NgIf,
    DecimalPipe,
    AsyncPipe,
    SongsModule,
  ]
})
export class FeedComponent implements OnInit {
  protected feedItems: FeedResponseModel = {
    songs: [],
    albums: []
  };

  constructor(private feedService: FeedService, protected imagesService: ImagesService, private router: Router) {
  }

  ngOnInit() {
    // this.loadFeed();
    this.loadMockFeed();

  }

  loadFeed() {
    this.feedService.getFeed().subscribe({
      next: (feed: FeedResponseModel) => {
        if (feed) {
          this.feedItems = feed;
          console.log('Feed loaded:', this.feedItems);

          const albums = feed.albums || [];
          const songs = feed.songs || [];

          const albumObservables = albums.map(a =>
            this.imagesService.getAlbumImageUrl(a.imageFile).pipe(
              catchError(() => of(null)),
              map(url => ({ ...a, imageUrl: url }))
            )
          );

          const songObservables = songs.map(s =>
            this.imagesService.getSongImageUrl(s.imageFile).pipe(
              catchError(() => of(null)),
              map(url => ({ ...s, imageUrl: url }))
            )
          );

          forkJoin(albumObservables).subscribe(albumResults => this.feedItems.albums = albumResults);
          forkJoin(songObservables).subscribe(songResults => this.feedItems.songs = songResults);
        }
      },
      error: (err: any) => {
        console.error('Error unsubscribing from artist:', err);
      }
    });
  }

  songLimit = 5;
  songPage = 1;

  getPaginatedSongs() {
    const start = (this.songPage - 1) * this.songLimit;
    return this.feedItems.songs.slice(start, start + this.songLimit);
  }

  hasNextSongPage(): boolean {
    return this.songPage * this.songLimit < this.feedItems.songs.length;
  }

  nextSongPage() {
    if (this.hasNextSongPage()) this.songPage++;
  }

  prevSongPage() {
    if (this.songPage > 1) this.songPage--;
  }

  scrollNext(list: HTMLElement) {
    list.scrollBy({ left: 300, behavior: 'smooth' });
  }

  scrollPrev(list: HTMLElement) {
    list.scrollBy({ left: -300, behavior: 'smooth' });
  }

  goToAlbumDetails(albumId: string) {
    this.router.navigate(['/albums/details', albumId]);
  }


  loadMockFeed() {
    const artistA: any = { artistId: 'a1', name: 'Artist A' };
    const artistB: any = { artistId: 'b2', name: 'Artist B' };
    const artistC: any = { artistId: 'c3', name: 'Artist C' };
    const now = new Date().toISOString();

    const songs: any[] = [
      { songId: '1', title: 'Song One', artist: artistA, otherArtists: [artistB], genres: ['pop'], fileKey: 'mock/path/song1.mp3', imageFile: 'mock/path/song1.jpg', ratingSum: 10, ratingCount: 2, createdAt: now, weighted_score: 0.9, timestamp: now },
      { songId: '2', title: 'Song Two', artist: artistB, otherArtists: [], genres: ['folk'], fileKey: 'mock/path/song2.mp3', imageFile: 'mock/path/song2.jpg', ratingSum: 20, ratingCount: 4, createdAt: now, weighted_score: 0.8, timestamp: now },
      { songId: '1', title: 'Song One', artist: artistA, otherArtists: [artistB], genres: ['pop'], fileKey: 'mock/path/song1.mp3', imageFile: 'mock/path/song1.jpg', ratingSum: 10, ratingCount: 2, createdAt: now, weighted_score: 0.9, timestamp: now },
      { songId: '2', title: 'Song Two', artist: artistB, otherArtists: [], genres: ['folk'], fileKey: 'mock/path/song2.mp3', imageFile: 'mock/path/song2.jpg', ratingSum: 20, ratingCount: 4, createdAt: now, weighted_score: 0.8, timestamp: now },
      { songId: '1', title: 'Song One', artist: artistA, otherArtists: [artistB], genres: ['pop'], fileKey: 'mock/path/song1.mp3', imageFile: 'mock/path/song1.jpg', ratingSum: 10, ratingCount: 2, createdAt: now, weighted_score: 0.9, timestamp: now },
      { songId: '2', title: 'Song Two', artist: artistB, otherArtists: [], genres: ['folk'], fileKey: 'mock/path/song2.mp3', imageFile: 'mock/path/song2.jpg', ratingSum: 20, ratingCount: 4, createdAt: now, weighted_score: 0.8, timestamp: now },
      { songId: '1', title: 'Song One', artist: artistA, otherArtists: [artistB], genres: ['pop'], fileKey: 'mock/path/song1.mp3', imageFile: 'mock/path/song1.jpg', ratingSum: 10, ratingCount: 2, createdAt: now, weighted_score: 0.9, timestamp: now },
      { songId: '2', title: 'Song Two', artist: artistB, otherArtists: [], genres: ['folk'], fileKey: 'mock/path/song2.mp3', imageFile: 'mock/path/song2.jpg', ratingSum: 20, ratingCount: 4, createdAt: now, weighted_score: 0.8, timestamp: now },
      { songId: '1', title: 'Song One', artist: artistA, otherArtists: [artistB], genres: ['pop'], fileKey: 'mock/path/song1.mp3', imageFile: 'mock/path/song1.jpg', ratingSum: 10, ratingCount: 2, createdAt: now, weighted_score: 0.9, timestamp: now },
      { songId: '2', title: 'Song Two', artist: artistB, otherArtists: [], genres: ['folk'], fileKey: 'mock/path/song2.mp3', imageFile: 'mock/path/song2.jpg', ratingSum: 20, ratingCount: 4, createdAt: now, weighted_score: 0.8, timestamp: now },
      { songId: '3', title: 'Song Three', artist: artistC, otherArtists: [], genres: ['rock'], fileKey: 'mock/path/song3.mp3', imageFile: 'mock/path/song3.jpg', ratingSum: 15, ratingCount: 3, createdAt: now, weighted_score: 0.7, timestamp: now },
    ];

    const albums: any[] = [
      { albumId: '1', title: 'Album One', artist: artistA, genres: ['pop'], imageFile: '1234.jpg', details: 'Description of Album One', tracks: [songs[0], songs[2]], createdAt: now, weighted_score: 0.95, timestamp: now },
      { albumId: '2', title: 'Album Two', artist: artistA, genres: ['pop'], imageFile: '1234.jpg', details: 'Description of Album One', tracks: [songs[0], songs[2]], createdAt: now, weighted_score: 0.95, timestamp: now },
      { albumId: '2', title: 'Album Two', artist: artistA, genres: ['pop'], imageFile: '1234.jpg', details: 'Description of Album One', tracks: [songs[0], songs[2]], createdAt: now, weighted_score: 0.95, timestamp: now },
      { albumId: '2', title: 'Album Two', artist: artistA, genres: ['pop'], imageFile: '1234.jpg', details: 'Description of Album One', tracks: [songs[0], songs[2]], createdAt: now, weighted_score: 0.95, timestamp: now },
      { albumId: '2', title: 'Album Two', artist: artistA, genres: ['pop'], imageFile: '1234.jpg', details: 'Description of Album One', tracks: [songs[0], songs[2]], createdAt: now, weighted_score: 0.95, timestamp: now },
      { albumId: '2', title: 'Album Two', artist: artistA, genres: ['pop'], imageFile: '1234.jpg', details: 'Description of Album One', tracks: [songs[0], songs[2]], createdAt: now, weighted_score: 0.95, timestamp: now },
      { albumId: '2', title: 'Album Two', artist: artistA, genres: ['pop'], imageFile: '1234.jpg', details: 'Description of Album One', tracks: [songs[0], songs[2]], createdAt: now, weighted_score: 0.95, timestamp: now },
      { albumId: '2', title: 'Album Two', artist: artistB, genres: ['folk'], imageFile: '1234.jpg', details: 'Description of Album Two', tracks: [songs[1]], createdAt: now, weighted_score: 0.85, timestamp: now },
    ];

    this.feedItems = { songs, albums };
}
}
