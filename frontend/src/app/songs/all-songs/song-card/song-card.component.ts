import { Component, Input, Output, EventEmitter } from '@angular/core';
import { Song } from '../../model/song.model';
import { Artist } from '../../../artists/model/artist.model';
import { SongService } from '../../service/song.service';

@Component({
  selector: 'app-song-card',
  templateUrl: './song-card.component.html',
  styleUrls: ['../../../shared/themes/card.css'],
  standalone: false
})
export class SongCardComponent {
  @Input() song!: Song;
  @Input() artists: Artist[] = []; // passed from parent (so you call ArtistService only once)
  
  @Output() edit = new EventEmitter<string>();
  @Output() delete = new EventEmitter<string>();
  @Output() favourite = new EventEmitter<string>();

  audio = new Audio();
  isPlaying = false;

  constructor(private songService: SongService) {}

  getArtistNames(): string {
    if (!this.song || !this.song.artistIds?.length) return 'Unknown artist';
    return this.song.artistIds
      .map(id => this.artists.find(a => a.artistId === id)?.name || 'Unknown artist')
      .join(', ');
  }

  playSong() {
    if (!this.song.file) return;

    if (this.isPlaying) {
      this.audio.pause();
      this.audio.currentTime = 0;
      this.isPlaying = false;
      return;
    }

    this.songService.getUrl(this.song.file).subscribe({
      next: (songUrl) => {
        this.audio.src = songUrl.url;
        this.audio.load();
        this.audio.play().then(() => {
          this.isPlaying = true;
        }).catch(err => console.error('Audio play failed:', err));

        this.audio.onended = () => this.isPlaying = false;
      },
      error: (err) => console.error('Failed to get song URL', err)
    });
  }



}
