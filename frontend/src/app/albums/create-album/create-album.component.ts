import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import {Album, AlbumTrack, CreateAlbumDTO, CreateTrackDTO, TrackDTO} from '../model/album.model';
import { ArtistService } from '../../artists/service/artist.service';
import { Artist } from '../../artists/model/artist.model';
import { AlbumService } from '../service/album.service';
import { DialogType } from '../../shared/dialog/dialog.component';
import { Genre } from '../../songs/model/genre.model';
import { GenreService } from '../../songs/service/genre.service';
import { ActivatedRoute } from '@angular/router';
import {CacheService} from '../../shared/cache/cache.service';

@Component({
  selector: 'app-create-album',
  templateUrl: './create-album.component.html',
  styleUrls: ['../../shared/themes/forms.css'],
  standalone: false
})
export class CreateAlbumComponent implements OnInit {
    album: CreateAlbumDTO = {
        title: '',
        artistId: "",
        genres: [],
        details: "",
        tracks: [],
        other: {}
    };

  imageDragging = false;
  imageFileName = '';
  uploadImageFile: File | undefined;

  selectedOtherArtist: { [key: number]: string } = {};
  editMode = false;
  editAlbumId: string | null | undefined;


  tracks: AlbumTrack[] = [{ title: '', file: undefined, dragging: false, otherArtistIds: []}];
  fileInputMap = new Map<AlbumTrack, HTMLInputElement>();

  artists: Artist[] = [];
  genres: Genre[] = [];

  genreInput = '';
  genreInputManual = '';
  otherKey = '';
  otherValue = '';

  loading = false;
  errorMessage = '';
  dialogType: DialogType = 'message';
  dialogTitle = '';
  dialogMessage = '';
  showDialog = false;

    constructor( private artistService: ArtistService, private genreService: GenreService, private albumService: AlbumService, private cache: CacheService, private route: ActivatedRoute) {}

    getArtistNameById(id: string): string {
      const artist = this.artists.find(a => a.artistId === id);
      return artist ? artist.name : '';
    }


  ngOnInit() {
        this.artistService.getAllRegular().subscribe(a=>
        {
          this.artists = a.artists;
        });
        this.genreService.getAll().subscribe(a=>
        {
          this.genres = a;
        });


    const albumId = this.route.snapshot.paramMap.get('id');
    this.editAlbumId = this.route.snapshot.paramMap.get('id');
    if (albumId) {
      this.editMode = true;
      this.albumService.getById(albumId).subscribe({
        next: albumData => {
          const other = { ...albumData.other };
          delete other['createdAt'];

          this.album = {
            title: albumData.title,
            artistId: albumData.artist?.artistId || '',
            genres: albumData.genres,
            details: albumData.details,
            other,
            tracks: albumData.tracks.map(t => ({
              songId: t.songId,
              title: t.title,
              file: undefined,
              otherArtistIds: t.otherArtistIds || []
            }))
          };

          console.log(this.album);

          // Initialize tracks if missing
          if (!this.album.tracks) {
            this.album.tracks = [];
          }

          // Load tracks to your local array for editing
          this.tracks = albumData.tracks.map((t: TrackDTO) => ({
            songId: t.songId,
            title: t.title,
            file: undefined, // user can reupload if needed
            dragging: false,
            otherArtistIds: t.otherArtistIds || []
          }));

          this.imageFileName = albumData.imageFile || '';
        },
        error: err => {
          console.error(err);
          this.showError('Error loading album data.');
        }
      });
    }
    }

    addGenre() {
        const value = this.genreInput.trim() || this.genreInputManual.trim();
        if (value && !this.album.genres.includes(value)) {
        this.album.genres.push(value);
        this.genreInput = '';
        this.genreInputManual = '';
        }
    }

    removeGenre(index: number) {
        this.album.genres.splice(index, 1);
    }


    addOther() {
        if (this.otherKey.trim()) {
        this.album.other![this.otherKey.trim()] = this.otherValue;
        this.otherKey = '';
        this.otherValue = '';
        }
    }

    removeOther(key: string) {
        delete this.album.other![key];
    }

  addTrack() {
    this.tracks.push({ title: '', file: undefined, dragging: false, otherArtistIds: [] });
  }


    removeTrack(index: number) {
        this.tracks.splice(index, 1);
    }

    onFileSelected(event: any, track: AlbumTrack) {
    const file = event.target.files[0];
    if (file) {
        track.file = file;
    }
    }

    onFileDropped(event: DragEvent, track: AlbumTrack) {
    event.preventDefault();
    track.dragging = false;
    if (event.dataTransfer && event.dataTransfer.files.length > 0) {
        track.file = event.dataTransfer.files[0];
    }
    }

    onDragOver(event: DragEvent, track: AlbumTrack) {
    event.preventDefault();
    track.dragging = true;
    }

    onDragLeave(event: DragEvent, track: AlbumTrack) {
    event.preventDefault();
    track.dragging = false;
    }

    async submit() {
      if (!this.album.title.trim() || this.album.artistId.length === 0 || this.album.genres.length === 0) {
          this.showError('Title, author Artist and Genre are required');
          return;
      }

        if (!this.album.details.trim()) {
          this.showError('Album details are required');
          return;
        }

        if (!this.editMode && !this.uploadImageFile) {
          this.showError('Album cover image is required');
          return;
        }


        for (let t of this.tracks) {
          if (!t.title.trim()) {
            this.showError('Each track must have a title');
            return;
          }
          if (!this.editMode && !t.file) {
            this.showError('Each track must have an audio file');
            return;
          }
        }

      this.loading = true;

      try {

        const tracksPayload: CreateTrackDTO[] = this.tracks.map((t) => {
            return {
              songId: t.songId,
              title: t.title.trim(),
              otherArtistIds: t.otherArtistIds
            };
        });

        const payload:CreateAlbumDTO = {
              title: this.album.title,
              artistId: this.album.artistId,
              genres: this.album.genres,
              tracks: tracksPayload,
            details: this.album.details.trim(),
          other: this.album.other
          };


        if (this.editMode) {
          if(this.editAlbumId != null){
            payload.albumId = this.editAlbumId
          }


          this.albumService.edit(payload).subscribe({
            next: async (res) => {
              console.log('Metadata saved, response:', res);
              if (this.uploadImageFile && res.imageUploadUrl) {
                await fetch(res.imageUploadUrl, {
                  method: 'PUT',
                  body: this.uploadImageFile,
                  headers: {
                    'Content-Type': 'image/png'
                  }
                });
              }


              if (res.trackUploadUrls && this.tracks) {
                const newTrackFiles = this.tracks
                  .filter(t => t.file && !t.songId)  // nove pesme
                  .map((t, idx) => ({ file: t.file!, url: res.trackUploadUrls[idx] }));
                console.log("New tracks to upload:", newTrackFiles);
                for (const t of newTrackFiles) {
                  await fetch(t.url, {
                    method: 'PUT',
                    body: t.file,
                    headers: { 'Content-Type': 'audio/mpeg' }
                  });
                }
              }

              // --- Upload overridden tracks ---
              if (res.trackOverrideUrls && this.tracks) {
                const overrideTracks = this.tracks
                  .filter(t => t.songId && t.file); // postojeći trackovi sa izmenjenim file
                console.log("Override tracks to upload:", overrideTracks);
                for (const t of overrideTracks) {
                  const url = res.trackOverrideUrls[t.songId!];
                  if (url) {
                    await fetch(url, {
                      method: 'PUT',
                      body: t.file,
                      headers: { 'Content-Type': 'audio/mpeg' }
                    });
                  }
                }
              }



              this.loading = false;
              this.showMessage(res.message);
              this.cache.clearCache();
            },
            error: (err) => {
              console.error(err);
              this.loading = false;
              this.showError('Error updating album.');
            }
          });
        } else {

          console.log("Album to be created")
          console.log(payload);
          this.albumService.create(payload).subscribe({
            next: async (res) => {
              console.log('Metadata saved, response:', res);
              for (let i = 0; i < this.tracks.length; i++) {
                const track = this.tracks[i];
                const urlInfo = res.trackUploadUrls[i];
                if (track.file && urlInfo) {
                  await fetch(urlInfo, {
                    method: 'PUT',
                    body: track.file,
                    headers: {
                      'Content-Type': 'audio/mpeg'
                    }
                  });
                }
              }

              if (this.uploadImageFile && res.imageUploadUrl) {
                await fetch(res.imageUploadUrl, {
                  method: 'PUT',
                  body: this.uploadImageFile,
                  headers: {
                    'Content-Type': 'image/png'
                  }
                });
              }

              this.loading = false;
              this.showMessage(res.message);
              this.cache.clearCache();
            },
            error: (err) => {
              console.error(err);
              this.loading = false;
              this.showError('Error creating the album.');
            }
          });

        }












      } catch (err) {
          console.error(err);
          this.loading = false;
          this.showError('Failed to convert files to Base64.');
      }







    }














    showError(message: string) {
        this.errorMessage = message;
        this.dialogType = 'error';
        this.dialogTitle = 'Validation Error';
        this.dialogMessage = message;
        this.showDialog = true;
    }

    showMessage(message: string) {
        this.dialogType = 'message';
        this.dialogTitle = 'Success';
        this.dialogMessage = message;
        this.showDialog = true;
    }

    closeDialog() {
        this.showDialog = false;
    }


  onImageSelected(event: any) {
    const file = event.target.files[0];
    if (file) {
      this.uploadImageFile = file;  // store the File object
      this.imageFileName = file.name;
    }
  }

  onImageDropped(event: DragEvent) {
    event.preventDefault();
    this.imageDragging = false;
    if (event.dataTransfer && event.dataTransfer.files.length > 0) {
      const file = event.dataTransfer.files[0];
      this.uploadImageFile = file;
      this.imageFileName = file.name;
    }
  }

  onImageDragOver(event: DragEvent) {
    event.preventDefault();
    this.imageDragging = true;
  }

  onImageDragLeave(event: DragEvent) {
    event.preventDefault();
    this.imageDragging = false;
  }

  addOtherArtist(track: AlbumTrack, artistId: string, index?: number) {
    if (artistId && !track.otherArtistIds?.includes(artistId)) {
      // Initialize if undefined
      if (!track.otherArtistIds) track.otherArtistIds = [];

      track.otherArtistIds.push(artistId);

      // Clear selected dropdown
      if (index !== undefined) {
        this.selectedOtherArtist[index] = '';
      }
    }
  }


  removeOtherArtist(track: AlbumTrack, artistId: string) {
    track.otherArtistIds = track.otherArtistIds?.filter(id => id !== artistId);
  }

}
