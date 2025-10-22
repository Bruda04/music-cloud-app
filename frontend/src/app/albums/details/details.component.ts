import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Album } from '../model/album.model';
import { AlbumService } from '../service/album.service';
import { TrackDTO } from '../model/album.model';
import { Artist } from '../../artists/model/artist.model';
import {UserRole} from '../../auth/model/user.model';
import {AuthService} from '../../auth/auth.service';
import {DialogType} from '../../shared/dialog/dialog.component';

@Component({
  selector: 'app-album-details',
  templateUrl: './details.component.html',
  styleUrls: ['./details.component.css'],
  standalone: false
})
export class AlbumDetailsComponent implements OnInit {
    album!: Album;
    artists: Artist[] = [];
    audio = new Audio();
    currentTrack?: string;
    isPlaying = false;

    photoPath: string = 'photo.jpg';

    showDialog = false;
    dialogType: DialogType = 'confirmation';
    dialogTitle = '';
    dialogMessage = '';
    pendingDeleteId: string | null = null;
    dialogRating: number = 0;

    constructor(private route: ActivatedRoute, private albumService: AlbumService, protected authService: AuthService) {}

    ngOnInit() {
        const navState = history.state;

        if (navState.album) {
            this.album = navState.album;
            this.artists = navState.artists || [];
        } else {
            const albumId = this.route.snapshot.paramMap.get('id');
            if (albumId) {
                this.albumService.getById(albumId).subscribe(album => {this.album = album;});
            }
        }
    }

    getArtistNames(): string {
        if (!this.album?.artistId?.length) return 'Unknown artist';
        return this.album.artistId
    }

    playTrack(track:TrackDTO) {
        if (!track.fileKey) return;

        if (this.isPlaying) {
            this.audio.pause();
            this.audio.currentTime = 0;
            this.isPlaying = false;
            return;
        }
        this.albumService.getUrl(track.fileKey).subscribe({
            next: (url) => {
                this.audio.src = url.url;
                this.audio.crossOrigin = 'anonymous';
                this.audio.load();
                this.audio.play().then(() => {
                    this.isPlaying = true;
                }).catch(err => console.error('Audio play failed:', err));

                this.audio.onended = () => this.isPlaying = false;
            },
            error: (err) => console.error('Failed to get track URL', err)
        });
    }

  protected readonly UserRole = UserRole;

  private ratingTrackId: string | null = null;

  rateTrack(track: TrackDTO, $event: PointerEvent) {
    $event.stopPropagation();
    this.ratingTrackId = track.songId;
    this.dialogType = 'rating';
    this.dialogTitle = 'Rate Track';
    this.dialogMessage = `Please rate the track "${track.title}":`;
    this.showDialog = true;
  }

  odTrackRated(rating: number) {
    this.dialogRating = rating;
    this.showDialog = false;

    if (this.dialogType === 'rating' && this.dialogRating > 0) {
      console.log('Submitting rating:', this.dialogRating);
      // if (this.album.albumId != null && this.ratingTrackId != null) {
      //   this.albumService.rateAlbumSong(this.ratingTrackId, this.album.albumId, this.dialogRating).subscribe({
      //     next: res => {
      //       this.dialogType = 'message';
      //       this.dialogTitle = 'Thank you!';
      //       this.dialogMessage = `You rated this track with ${this.dialogRating} stars.`;
      //       this.showDialog = true;
      //     },
      //     error: err => {
      //       this.dialogType = 'error';
      //       this.dialogTitle = 'Error';
      //       this.dialogMessage = err.error?.message || 'Failed to submit rating';
      //       this.showDialog = true;
      //     }
      //   });
      // }
      this.dialogRating = 0;
      return;
    }
  }

  onDialogClosed(confirmed: boolean) {

  }
}
