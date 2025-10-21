import { Component, Input, OnInit } from '@angular/core';
import { Song } from '../model/song.model';
import { SongService } from '../service/song.service';
import { Artist } from '../../artists/model/artist.model';
import { SongsModule } from '../songs.module';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-all-songs',
  templateUrl: './all-songs.component.html',
  styleUrls: ['../../shared/themes/all-items.css'],
  imports: [SongsModule,CommonModule],
  standalone: true
})
export class AllSongsComponent implements OnInit {
  @Input() artists: Artist[] = [];

  songs: Song[] = [];
  pageKeys: (string | undefined)[] = [undefined]; // pageKeys[0] = first page start = undefined
  page = 1;
  limit = 5;

  constructor(private songService: SongService) {}

  ngOnInit() {
    this.loadSongs(this.page);
  }

  loadSongs(page: number) {
    const lastKey = this.pageKeys[page - 1]; // start key for the requested page

    this.songService.getSongs(this.limit, lastKey).subscribe(res => {
      if (res.songs.length === 0 && page > 1) {
        // If no songs, do not move page forward
        return;
      }

      this.songs = res.songs;
      this.page = page;

      // Store lastKey for the next page
      if (res.lastKey) {
        this.pageKeys[page] = res.lastKey;
      } else {
        this.pageKeys[page] = undefined;
      }
    });
  }

  nextPage() {
    this.loadSongs(this.page + 1);
  }

  prevPage() {
    if (this.page > 1) {
      this.loadSongs(this.page - 1);
    }
  }

  onSongDeleted(id: string) {
    this.loadSongs(this.page);
  }

  onRate(id: string) {
    console.log('Rate', id);
  }
}
