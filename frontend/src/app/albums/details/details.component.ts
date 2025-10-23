import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Album } from '../model/album.model';
import { AlbumService } from '../service/album.service';
import { TrackDTO } from '../model/album.model';
import { Artist } from '../../artists/model/artist.model';
import {UserRole} from '../../auth/model/user.model';
import {AuthService} from '../../auth/auth.service';
import {DialogType} from '../../shared/dialog/dialog.component';
import {CacheService} from '../../shared/cache/cache.service';
import {ImagesService} from '../../shared/images/service/images.service';

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

    photoPath: string | undefined = 'photo.png';

    showDialog = false;
    dialogType: DialogType = 'confirmation';
    dialogTitle = '';
    dialogMessage = '';
    dialogRating: number = 0;

    constructor(private route: ActivatedRoute, private albumService: AlbumService, protected authService: AuthService, private  cacheService: CacheService, private imageService: ImagesService) {}

    ngOnInit() {
        const navState = history.state;

        if (navState.album) {
            this.album = navState.album;
            //this.album.tracks[0].ratingCount = 2
            //this.album.tracks[0].ratingSum = 9
            this.artists = navState.artists || [];
        } else {
            const albumId = this.route.snapshot.paramMap.get('id');
            if (albumId) {
                this.albumService.getById(albumId).subscribe(album => {this.album = album;});
            }
        }

        this.loadImage();
      console.log(this.album);
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

        this.logPlay(track);

      const cached = this.cacheService.getTrack(track.songId!);
      if (cached) {
        console.log('Playing from cache');
        this.audio.src = cached.data; // Base64 data URL
        this.audio.play().then(() => {
          this.currentTrack = track.songId;
          this.isPlaying = true
        })
          .catch(err => console.error(err));
        this.audio.onended = () => {
          this.isPlaying = false
          this.currentTrack = undefined;
        };

        return;
      }


        this.albumService.getUrl(track.fileKey).subscribe({
            next: async (url) => {
              try {
                const response = await fetch(url.url);
                const blob = await response.blob();
                this.cacheService.saveTrack(track.songId!, track.title + '.mp3', blob);
                console.log('Song cached');

                console.log('Playing from cache after fetch');
                this.audio.src = URL.createObjectURL(blob);
                this.audio.play().then(() => {
                  this.isPlaying = true
                  this.currentTrack = track.songId;
                })
                  .catch(err => console.error(err));
                this.audio.onended = () => {
                  this.isPlaying = false
                  this.currentTrack = undefined;
                };

              } catch (err) {
                console.error('Failed to play song', err);
              }
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

  private loadImage() {
    if (this.album && this.album.imageFile) {
      this.imageService.getAlbumImageUrl(this.album.imageFile).subscribe({
        next: (url: string) => {
          this.photoPath = url;
        },
        error: (err: any) => {
          console.error('Error loading album image:', err);
        }
      });
    }
  }


  odTrackRated(rating: number) {
    this.dialogRating = rating;
    this.showDialog = false;

    if (this.dialogType === 'rating' && this.dialogRating > 0) {
      console.log('Submitting rating:', this.dialogRating);
      if (this.album.albumId != null && this.ratingTrackId != null) {
        this.albumService.rateAlbumSong(this.ratingTrackId, this.album.albumId, this.dialogRating).subscribe({
          next: res => {
            this.dialogType = 'message';
            this.dialogTitle = 'Thank you!';
            this.dialogMessage = `You rated this track successfully.`;
            this.showDialog = true;
          },
          error: err => {
            this.dialogType = 'error';
            this.dialogTitle = 'Error';
            this.dialogMessage = err.error?.message || 'Failed to submit rating';
            this.showDialog = true;
          }
        });
      }
      this.dialogRating = 0;
      return;
    }
  }

  onDialogClosed(confirmed: boolean) {
    this.showDialog = false;

  }

  downloadTrack(track:TrackDTO, $event: PointerEvent) {
    $event.stopPropagation();
    if (!track.fileKey) return;

    this.albumService.getUrl(track.fileKey).subscribe({
      next: async (res) => {
        try {
          // fetch the file as blob
          const response = await fetch(res.url);
          const blob = await response.blob();

          // create a temporary URL
          const blobUrl = URL.createObjectURL(blob);

          const link = document.createElement('a');
          link.href = blobUrl;
          link.download = track.title + '.mp3';
          document.body.appendChild(link);
          link.click();
          document.body.removeChild(link);

          // revoke object URL
          URL.revokeObjectURL(blobUrl);
        } catch (err) {
          console.error('Failed to download track', err);
        }
      },
      error: (err) => console.error('Failed to get track URL', err)
    });
  }

  logPlay(track: TrackDTO) {
    if (!track.songId || !this.album.albumId) return;
    this.albumService.logPlay(this.album.albumId, track.songId, this.album.artistId)
  }
}
