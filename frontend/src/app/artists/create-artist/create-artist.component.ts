import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { ArtistService } from '../service/artist.service';
import { Artist } from '../model/artist.model';
import { DialogType } from '../../shared/dialog/dialog.component';

@Component({
  selector: 'app-create-artist',
  templateUrl: './create-artist.component.html',
  styleUrls: ['../../shared/themes/forms.css'],
  standalone:false
})
export class CreateArtistComponent {
  artist: Artist = {
    name: '',
    bio: '',
    genres: [],
    other: {}
  };

  genreInput = '';
  otherKey = '';
  otherValue = '';
  
  loading = false;
  errorMessage = '';
  dialogType: DialogType = 'message';
  dialogTitle = '';
  dialogMessage = '';
  showDialog = false;

  constructor(private artistService: ArtistService, private router: Router) {}

  addGenre() {
    if (this.genreInput.trim()) {
      this.artist.genres.push(this.genreInput.trim());
      this.genreInput = '';
    }
  }

  removeGenre(index: number) {
    this.artist.genres.splice(index, 1);
  }

  addOther() {
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
    this.artistService.createArtist(this.artist).subscribe({
      next: res => {
        console.log('Artist created:', res.artist);
        this.loading = false;
        this.dialogType = 'message';
        this.dialogTitle = 'Success';
        this.dialogMessage = 'Artist successfully created!';
        this.showDialog = true;
      },
      error: err => {
        console.error(err);
        this.loading = false;
        this.dialogType = 'error';
        this.dialogTitle = 'Error';
        this.dialogMessage = 'Error creating an artist.';
        this.showDialog = true;
      }
    });
  }

  closeDialog() {
    this.showDialog = false;
  }
}
