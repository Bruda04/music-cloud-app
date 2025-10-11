import { Component, Input, Output, EventEmitter } from '@angular/core';
import { Song } from '../../model/song.model';
import { Artist } from '../../../artists/model/artist.model';
import { SongService } from '../../service/song.service';
import { Router } from '@angular/router';
import { DialogType } from '../../../shared/dialog/dialog.component';

@Component({
  selector: 'app-song-card',
  templateUrl: './song-card.component.html',
  styleUrls: ['../../../shared/themes/card.css'],
  standalone: false
})
export class SongCardComponent {
  @Input() song!: Song;
  @Input() artists: Artist[] = []; // passed from parent (so you call ArtistService only once)
  
  @Output() favourite = new EventEmitter<string>();
  @Output() deleted = new EventEmitter<string>();

  audio = new Audio();
  isPlaying = false;

  showDialog = false;
  dialogType: DialogType = 'confirmation';
  dialogTitle = '';
  dialogMessage = '';
  pendingDeleteId: string | null = null;


  constructor(private songService: SongService,private router:Router) {}

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
  
  goToEdit() {
    if (this.song){
      this.router.navigate(['/songs/edit', this.song.songId]);
    }
  }
  
  deleteSong() {
    if (!this.song?.songId) return;

    this.dialogType = 'confirmation';
    this.dialogTitle = 'Are you sure?';
    this.dialogMessage = `Do you really want to delete "${this.song.title}"?`;
    this.pendingDeleteId = this.song.songId;
    this.showDialog = true;
  }

  onDialogClosed(confirmed: boolean) {
    this.showDialog = false;

    if (confirmed && this.pendingDeleteId) {
      this.songService.delete(this.pendingDeleteId).subscribe({
        next: res => {
          this.deleted.emit(this.pendingDeleteId!); 
          this.dialogType = 'message';
          this.dialogTitle = 'Deleted';
          this.dialogMessage = res.message;
          this.showDialog = true;
        },
        error: err => {
          this.dialogType = 'error';
          this.dialogTitle = 'Error';
          this.dialogMessage = err.error?.message || 'Failed to delete song';
          this.showDialog = true;
        }
      });
    }

    this.pendingDeleteId = null;
  }

}
