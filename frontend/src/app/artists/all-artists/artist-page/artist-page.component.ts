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
import {Album} from '../../../albums/model/album.model';

@Component({
  selector: 'app-artist-page',
  imports: [CommonModule, SongsModule, AlbumsModule],
  templateUrl: './artist-page.component.html',
  styleUrls: ['./artist-page.component.scss']
})
export class ArtistPageComponent implements OnInit {
  artist: Artist | undefined;
  content : { albums: Album[]; songs: Song[]; } | undefined;


constructor(
    private route: ActivatedRoute,
    public artistService: ArtistService,
  ) {}

  ngOnInit(): void {
    this.artist = history.state.artist;

    this.loadContent();
  }

  loadContent() {
    this.artistService.getArtistContent(this.artist?.artistId) .subscribe(a=>
    {
      this.content = a;
    });

  }

  playSong(song: Song) {
    console.log('Play song:', song.title);
    // You could integrate a player here
  }


  onSongDeleted(id: string) {
    this.loadContent()
  }
  onRate(id: string) { console.log('Rate', id); }
}
