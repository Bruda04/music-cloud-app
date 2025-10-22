import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import {Album, AlbumTrack, CreateAlbumDTO, CreateTrackDTO, TrackDTO} from '../model/album.model';
import { ArtistService } from '../../artists/service/artist.service';
import { Artist } from '../../artists/model/artist.model';
import { AlbumService } from '../service/album.service';
import { DialogType } from '../../shared/dialog/dialog.component';
import { Genre } from '../../songs/model/genre.model';
import { GenreService } from '../../songs/service/genre.service';

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
        imageFile: "",
        details: "",
        tracks: [],
        other: {}
    };

  imageDragging = false;
  imageFileName = '';
  uploadImageFile: File | undefined;

  selectedOtherArtist: { [key: number]: string } = {};


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

    constructor( private artistService: ArtistService, private genreService: GenreService, private albumService: AlbumService, private router: Router) {}

    getArtistNameById(id: string): string {
      const artist = this.artists.find(a => a.artistId === id);
      return artist ? artist.name : '';
    }


  ngOnInit() {
        this.artistService.getAll().subscribe(a=>
        {
          this.artists = a.artists;
        });
        this.genreService.getAll().subscribe(a=>
        {
          this.genres = a;
        });
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

        if (!this.uploadImageFile) {
          this.showError('Album cover image is required');
          return;
        }


        for (let t of this.tracks) {
          if (!t.title.trim() || !t.file) {
          this.showError('Each track must have a title and an audio file');
          return;
          }
      }

      this.loading = true;

      try {

        const tracksPayload: CreateTrackDTO[] = await Promise.all(
          this.tracks.map(async (t) => ({
            title: t.title.trim(),
            file: await this.convertFileToBase64(t.file!),
            otherArtistsId: t.otherArtistIds
          }))
        );


        let imageBase64 = "";
        if(this.uploadImageFile) {
           imageBase64 = await this.convertFileToBase64(this.uploadImageFile);
        }

        const payload:CreateAlbumDTO = {
              title: this.album.title,
              artistId: this.album.artistId,
              genres: this.album.genres,
              imageFile: imageBase64,
              tracks: tracksPayload,
            details: this.album.details.trim(),
          other: this.album.other
          };

          console.log("Album to be created")
          console.log(payload);
          this.albumService.create(payload).subscribe({
          next: (res) => {
              this.loading = false;
              this.showMessage(res.message);
          },
          error: (err) => {
              console.error(err);
              this.loading = false;
              this.showError('Error creating the album.');
          }
          });
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

    convertFileToBase64(file: File): Promise<string> {
        return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = () => {
            const result = reader.result as string;
            const base64 = result.split(',')[1];
            resolve(base64);
        };
        reader.onerror = error => reject(error);
        });
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
