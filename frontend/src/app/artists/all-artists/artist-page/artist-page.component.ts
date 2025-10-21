import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import {Artist} from '../../model/artist.model';
import {Song} from '../../../songs/model/song.model';
import {SongService} from '../../../songs/service/song.service';
import {CommonModule} from '@angular/common';
import {SongsModule} from '../../../songs/songs.module';
import {AlbumService} from '../../../albums/service/album.service';
import {AlbumsModule} from '../../../albums/albums.module';
import {ArtistService} from '../../service/artist.service';

@Component({
  selector: 'app-artist-page',
  imports: [CommonModule, SongsModule, AlbumsModule],
  templateUrl: './artist-page.component.html',
  styleUrls: ['./artist-page.component.scss']
})
export class ArtistPageComponent implements OnInit {
  artist: Artist | undefined;
  content :any;


constructor(
    private route: ActivatedRoute,
    private songService: SongService,
    private albumService: AlbumService,
    public artistService: ArtistService,
  ) {}

  ngOnInit(): void {
    // Get artist data from route state (like your album navigation)
    this.artist = history.state.artist;
    this.content = {"albums": this.albumService.getAll(), "songs": this.songService.getMockSongs()}

    // Load songs for this artist
    this.loadSongs();
  }

  loadSongs(lastKey?: string) {
    // Mocking for now
    // TODO: replace with actual API
    // this.songService.getSongs(this.artist?.artistId, lastKey).subscribe(res => {
    //     this.songs = res.songs;
    //     this.lastKey = res.lastKey;
    // });
  }

  playSong(song: Song) {
    console.log('Play song:', song.title);
    // You could integrate a player here
  }


  onSongDeleted(id: string) {
    this.loadSongs()
  }
  onRate(id: string) { console.log('Rate', id); }
}
