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
    @Input() artists: Artist[] = []; // with this i will have only one call on it
    songs: Song[] = [];
    lastKey?: string;
    limit = 5;
    page = 1;

    constructor(private songService: SongService) {}

    ngOnInit() {
        this.loadSongs();
    }

    loadSongs(lastKey?: string) {
        this.songService.getSongs(this.limit, lastKey).subscribe(res => {
            console.log(res)
            this.songs = res.songs;
            this.lastKey = res.lastKey;
        });
        // this.songs=this.songService.getMockSongs(); //TODO: change to getSongs, now is mock due to too many requests
    }

    nextPage() {
        if (this.lastKey) {
        this.page++;
        this.loadSongs(this.lastKey);
        }
    }

    prevPage() {
        if (this.page > 1) {
        this.page--;
        this.loadSongs();
        }
    }

    onEdit(id: string) { console.log('Edit', id); }
    onDelete(id: string) { console.log('Delete', id); }
    onFavourite(id: string) { console.log('Favourite', id); }
}
