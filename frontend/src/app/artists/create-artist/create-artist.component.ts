import { Component } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { ArtistService } from '../service/artist.service';
import { Artist } from '../model/artist.model';
import { DialogType } from '../../shared/dialog/dialog.component';
import { Genre } from '../../songs/model/genre.model';
import { GenreService } from '../../songs/service/genre.service';

@Component({
  selector: 'app-create-artist',
  templateUrl: './create-artist.component.html',
  styleUrls: ['../../shared/themes/forms.css'],
  standalone:false
})
export class CreateArtistComponent {
  editMode = false;
  artist: Artist = {
    name: '',
    bio: '',
    genres: [],
    other: {}
  };

  genreInput = '';
  genreInputManual = '';
  genres: Genre[] = [];

  otherKey = '';
  otherValue = '';

  loading = false;
  errorMessage = '';
  dialogType: DialogType = 'message';
  dialogTitle = '';
  dialogMessage = '';
  showDialog = false;

constructor(private artistService: ArtistService, private genreService:GenreService,private route: ActivatedRoute) {
    this.genreService.getAll().subscribe(g => this.genres = g);
    const artistId = this.route.snapshot.paramMap.get('id');
    if (artistId) {
      this.editMode = true;
      this.artistService.getById(artistId).subscribe({
        next: artistData => {
          this.artist = artistData;
        },
        error: err => {
          console.error(err);
          this.errorMessage = 'Error loading artist data.';
          this.dialogType = 'error';
          this.dialogTitle = 'Error';
          this.dialogMessage = this.errorMessage;
          this.showDialog = true;
        }
      });
    }
  }

  addGenre() {
    const selected = this.genreInput.trim();
    const manual = this.genreInputManual.trim();
    const value = selected || manual;

    if (value && !this.artist.genres.includes(value)) {
      this.artist.genres.push(value);
      this.genreInput = '';
      this.genreInputManual = '';
    }
  }

  removeGenre(index: number) {
    this.artist.genres.splice(index, 1);
  }

  addOther() {
    if (!this.artist.other) {
      this.artist.other = {}; // Initialize if undefined
    }
    if (this.otherKey.trim()) {
      this.artist.other![this.otherKey.trim()] = this.otherValue;
      this.otherKey = '';
      this.otherValue = '';
    }
  }

  removeOther(key: string) {
    delete this.artist.other![key];
  }

  submit() {
    if (!this.artist.name.trim() || !this.artist.bio.trim() || this.artist.genres.length === 0) {
      this.errorMessage = 'Name, Bio and at least one Genre are required';
      this.dialogType = 'error';
      this.dialogTitle = 'Validation Error';
      this.dialogMessage = this.errorMessage;
      this.showDialog = true;
      return;
    }

    this.loading = true;

    if (this.artist.artistId){
      console.log('Editing artist:', this.artist);
      this.artistService.editArtist(this.artist).subscribe({
        next: res => {
          console.log('Artist edited:', res.artistId);
          this.loading = false;
          this.dialogType = 'message';
          this.dialogTitle = 'Success';
          this.dialogMessage = res.message.toString();
          this.showDialog = true;
        },
        error: err => {
          console.error(err);
          this.loading = false;
          this.dialogType = 'error';
          this.dialogTitle = 'Error';
          this.dialogMessage = 'Error updating artist.';
          this.showDialog = true;
        }
      });
    }
    else{
      this.artistService.createArtist(this.artist).subscribe({
        next: res => {
          console.log('Artist created:', res.artist);
          this.loading = false;
          this.dialogType = 'message';
          this.dialogTitle = 'Success';
          this.dialogMessage = res.message.toString();
          this.showDialog = true;
        },
        error: err => {
          console.error(err);
          this.loading = false;
          this.dialogType = 'error';
          this.dialogTitle = 'Error';
          this.dialogMessage = 'Error creating artist.';
          this.showDialog = true;
        }
      });
    }
  }

  closeDialog() {
    this.showDialog = false;
  }
}
