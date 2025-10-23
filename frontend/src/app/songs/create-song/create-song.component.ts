import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { DialogType } from '../../shared/dialog/dialog.component';
import { Song } from '../model/song.model';
import { SongService } from '../service/song.service';
import { ArtistService } from '../../artists/service/artist.service';
import { Artist } from '../../artists/model/artist.model';
import { GenreService } from '../service/genre.service';
import { Genre } from '../model/genre.model';
import {CacheService} from '../../shared/cache/cache.service';

@Component({
  selector: 'app-create-song',
  templateUrl: './create-song.component.html',
  styleUrls: ['../../shared/themes/forms.css'],
  standalone: false
})
export class CreateSongComponent implements OnInit {
  editMode = false;
  uploadedImage?: File;
  draggingImage = false;

  song: Song = {
    title: '',
    artist: { artistId: '', name: '' },
    otherArtists: [],
    genres: [],
    file: '',
    other: {}
  };

  artists: Artist[] = [];
  genres: Genre[] = [];

  artistInput: Artist | null = null; // za main artist
  otherArtistInput: Artist | null = null; // za other artists
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

  uploadedFile?: File;
  dragging = false;

  constructor(
    private songService: SongService,
    private artistService: ArtistService,
    private genreService: GenreService,
    private route: ActivatedRoute,
    private cacheService: CacheService,
  ) {}

  ngOnInit() {
    this.artistService.getAllRegular().subscribe(artists => {
      this.artists = artists.artists;
    });

    this.genreService.getAll().subscribe(genres => {
      this.genres = genres;
    });

    const songId = this.route.snapshot.paramMap.get('id');
    console.log('Song ID from route:', songId);
    if (songId) {
      this.editMode = true;
      this.songService.getById(songId).subscribe(res => {
        const other = { ...res.other };
        delete other['createdAt'];
        this.song = res;
        this.song.other = other;
        console.log('Loaded song for editing:', this.song);
      });
    }
  }

  setMainArtist() {
    if (this.artistInput) {
      this.song.artist = {
        artistId: this.artistInput.artistId || '',
        name: this.artistInput.name || ''
      };
      this.artistInput = null;
    }
  }

  removeMainArtist() {
    this.song.artist = { artistId: '', name: '' };
  }

  addOtherArtist() {
    if (
      this.otherArtistInput &&
      !this.song.otherArtists?.some(a => a.artistId === this.otherArtistInput!.artistId)
    ) {
      this.song.otherArtists?.push({
        artistId: this.otherArtistInput.artistId || '',
        name: this.otherArtistInput.name || ''
      });
      this.otherArtistInput = null;
    }
  }

  removeOtherArtist(index: number) {
    this.song.otherArtists?.splice(index, 1);
  }

  addGenre() {
    const selected = this.genreInput.trim();
    const manual = this.genreInputManual.trim();
    const value = selected || manual;

    if (value && !this.song.genres.includes(value)) {
      this.song.genres.push(value);
      this.genreInput = '';
      this.genreInputManual = '';
    }
  }

  removeGenre(index: number) {
    this.song.genres.splice(index, 1);
  }

  addOther() {
    if (this.otherKey.trim()) {
      this.song.other![this.otherKey.trim()] = this.otherValue;
      this.otherKey = '';
      this.otherValue = '';
    }
  }

  removeOther(key: string) {
    delete this.song.other![key];
  }

  async submit() {
    if (!this.song.title.trim() || !this.song.artist?.artistId || this.song.genres.length === 0) {
      this.showValidationError('Title, main Artist, and at least one Genre are required');
      return;
    }

    if (!this.editMode && !this.uploadedFile) {
      this.showValidationError('You must upload an mp3 file');
      return;
    }

    this.loading = true;

    try {
      if (this.uploadedFile || this.uploadedImage) {
        this.song.fileChanged = true;
      } else {
        this.song.fileChanged = false;
      }


      const payload: any = {
        songId: this.song.songId ? this.song.songId : undefined,
        title: this.song.title,
        artistId: this.song.artist?.artistId,
        otherArtistIds: this.song.otherArtists?.map(a => a.artistId),
        genres: this.song.genres,
        fileChanged: this.song.fileChanged,
        other: this.song.other
      };

      const req = this.editMode
        ? this.songService.edit(payload)
        : this.songService.create(payload);

      req.subscribe({
        next: async (res) => {
          try {
            console.log('Metadata saved, response:', res);
            if (this.uploadedFile && res.songUploadUrl) {
              await fetch(res.songUploadUrl, {
                method: 'PUT',
                body: this.uploadedFile,
                headers: {
                  'Content-Type': 'audio/mpeg'
                }
              });

            }

            if (this.uploadedImage && res.imageUploadUrl) {
              await fetch(res.imageUploadUrl, {
                method: 'PUT',
                body: this.uploadedImage,
                headers: {
                  'Content-Type': 'image/png'
                }
              });
            }

            this.loading = false;
            this.dialogType = 'message';
            this.dialogTitle = 'Success';
            this.dialogMessage = 'Song metadata saved and files uploaded successfully.';
            this.showDialog = true;
            this.cacheService.clearCache();

          } catch (uploadErr) {
            console.error('Upload failed:', uploadErr);
            this.loading = false;
            this.dialogType = 'error';
            this.dialogTitle = 'Upload Error';
            this.dialogMessage = 'Metadata saved, but file upload failed.';
            this.showDialog = true;
          }
        },
        error: (err) => {
          console.error(err);
          this.loading = false;
          this.dialogType = 'error';
          this.dialogTitle = 'Error';
          this.dialogMessage = 'Error creating song metadata.';
          this.showDialog = true;
        }
      });
    } catch (err) {
      console.error(err);
      this.loading = false;
      this.dialogType = 'error';
      this.dialogTitle = 'Error';
      this.dialogMessage = 'Unexpected error occurred.';
      this.showDialog = true;
    }
  }
  closeDialog() {
    this.showDialog = false;
  }

  getArtistNameById(aId: string): string {
    const artist = this.artists.find(a => a.artistId === aId);
    return artist ? artist.name : aId;
  }

  onFileDropped(event: DragEvent) {
    event.preventDefault();
    this.dragging = false;
    if (event.dataTransfer && event.dataTransfer.files.length > 0) {
      this.uploadedFile = event.dataTransfer.files[0];
    }
  }

  onFileSelected(event: any) {
    const file = event.target.files[0];
    if (file) {
      this.uploadedFile = file;
    }
  }

  onDragOver(event: DragEvent) {
    event.preventDefault();
    this.dragging = true;
  }

  onDragLeave(event: DragEvent) {
    event.preventDefault();
    this.dragging = false;
  }

  onImageDropped(event: DragEvent) {
  event.preventDefault();
  this.draggingImage = false;
  if (event.dataTransfer && event.dataTransfer.files.length > 0) {
    this.uploadedImage = event.dataTransfer.files[0];
  }
}

onImageSelected(event: any) {
  const file = event.target.files[0];
  if (file) {
    this.uploadedImage = file;
  }
}

onDragOverImage(event: DragEvent) {
  event.preventDefault();
  this.draggingImage = true;
}

onDragLeaveImage(event: DragEvent) {
  event.preventDefault();
  this.draggingImage = false;
}


  private showValidationError(message: string) {
    this.errorMessage = message;
    this.dialogType = 'error';
    this.dialogTitle = 'Validation Error';
    this.dialogMessage = message;
    this.showDialog = true;
  }
}
