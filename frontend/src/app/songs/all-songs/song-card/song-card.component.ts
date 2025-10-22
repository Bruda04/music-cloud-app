import { Component, Input, Output, EventEmitter } from '@angular/core';
import { Song } from '../../model/song.model';
import { Artist } from '../../../artists/model/artist.model';
import { SongService } from '../../service/song.service';
import { Router } from '@angular/router';
import { DialogType } from '../../../shared/dialog/dialog.component';
import {AuthService} from '../../../auth/auth.service';
import {UserRole} from '../../../auth/model/user.model';
import {CacheService} from '../../../shared/cache/cache.service';

@Component({
  selector: 'app-song-card',
  templateUrl: './song-card.component.html',
  styleUrls: ['../../../shared/themes/card.css'],
  standalone: false
})
export class SongCardComponent {
  @Input() song!: Song;
  @Input() artists: Artist[] = []; // passed from parent (so you call ArtistService only once)

  @Output() rate = new EventEmitter<string>();
  @Output() deleted = new EventEmitter<string>();

  photoPath: string = 'photo.jpg'; // placeholder image


  audio = new Audio();
  isPlaying = false;

  showDialog = false;
  dialogType: DialogType = 'confirmation';
  dialogTitle = '';
  dialogMessage = '';
  pendingDeleteId: string | null = null;
  dialogRating: number = 0;


  constructor(private songService: SongService,private router:Router, protected authService: AuthService, private cacheService: CacheService) {}

  playSong() {
    if (!this.song.file) return;

    if (this.isPlaying) {
      this.audio.pause();
      this.audio.currentTime = 0;
      this.isPlaying = false;
      return;
    }

    this.logPlay();

    const cached = this.cacheService.getTrack(this.song.songId!);
    if (cached) {
      console.log('Playing from cache');
      this.audio.src = cached.data; // Base64 data URL
      this.audio.play().then(() => this.isPlaying = true)
        .catch(err => console.error(err));
      this.audio.onended = () => this.isPlaying = false;
      return;
    }

    this.songService.getUrl(this.song.file).subscribe(async (res) => {
      try {
        const response = await fetch(res.url);
        const blob = await response.blob();
        this.cacheService.saveTrack(this.song.songId!, this.song.title + '.mp3', blob);
        console.log('Song cached');

        console.log('Playing from cache after fetch');
        this.audio.src = URL.createObjectURL(blob);
        this.audio.play().then(() => this.isPlaying = true)
          .catch(err => console.error(err));
        this.audio.onended = () => this.isPlaying = false;

      } catch (err) {
        console.error('Failed to play song', err);
      }
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


  formatDate(dateString: string): string {
    if (!dateString) return '';
    const date = new Date(dateString);
    // Example: "Oct 20, 2025, 21:15"
    return date.toLocaleString(undefined, {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  }

  protected readonly UserRole = UserRole;


  rateSong() {
    this.dialogMessage = `Rate the song "${this.song.title}"`;
    this.dialogType = 'rating';
    this.dialogTitle = 'Rate Song';
    this.showDialog = true;


  }

  onSongRated(rating: number) {
    this.dialogRating = rating;
    this.showDialog = false;
    if (this.dialogType === 'rating' && this.dialogRating > 0) {
      console.log('Submitting rating:', this.dialogRating);
      // this.songService.rateSong(this.song.songId!, this.dialogRating).subscribe({
      //   next: res => {
      //     this.dialogType = 'message';
      //     this.dialogTitle = 'Thank you!';
      //     this.dialogMessage = `You rated "${this.song.title}" with ${this.dialogRating} stars.`;
      //     this.showDialog = true;
      //   },
      //   error: err => {
      //     this.dialogType = 'error';
      //     this.dialogTitle = 'Error';
      //     this.dialogMessage = err.error?.message || 'Failed to submit rating';
      //     this.showDialog = true;
      //   }
      // });
      this.dialogRating = 0;
    }
  }

  downloadSong() {
    if (!this.song.file) return;

    this.songService.getUrl(this.song.file).subscribe({
      next: async (res) => {
        try {
          // fetch the file as blob
          const response = await fetch(res.url);
          const blob = await response.blob();

          // create a temporary URL
          const blobUrl = URL.createObjectURL(blob);

          const link = document.createElement('a');
          link.href = blobUrl;
          link.download = this.song.title + '.mp3';
          document.body.appendChild(link);
          link.click();
          document.body.removeChild(link);

          // revoke object URL
          URL.revokeObjectURL(blobUrl);
        } catch (err) {
          console.error('Failed to download song', err);
        }
      },
      error: (err) => console.error('Failed to get song URL', err)
    });

  }

  private logPlay() {
    if (!this.song.songId || !this.song.artist?.artistId) return;
    this.songService.logPlay(this.song.songId, this.song.artist?.artistId);
  }
}
