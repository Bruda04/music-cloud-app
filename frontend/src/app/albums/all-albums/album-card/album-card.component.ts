import {Component, Input, OnInit} from '@angular/core';
import { Album } from '../../model/album.model';
import { Artist } from '../../../artists/model/artist.model';
import { Router } from '@angular/router';
import {UserRole} from '../../../auth/model/user.model';
import {AuthService} from '../../../auth/auth.service';
import {DialogType} from '../../../shared/dialog/dialog.component';
import {CommonModule} from '@angular/common';

@Component({
  selector: 'app-album-card',
  templateUrl: './album-card.component.html',
  standalone: false,
  styleUrls: ['../../../shared/themes/card.css']
})
export class AlbumCardComponent implements OnInit {
  @Input() album: Album | undefined;
  photoPath: string | undefined = "";


  showDialog = false;
  dialogType: DialogType = 'confirmation';
  dialogTitle = '';
  dialogMessage = '';


  constructor(private router:Router,  protected authService: AuthService){}

  ngOnInit() {
    this.photoPath = "photo.jpg"
  }

  openAlbum() {
    if (!this.album || !this.album.albumId) {
      console.error('Album ID is missing:', this.album);
      return;
    }
    this.router.navigate(['/albums/details/', this.album.albumId], {
      state: { album: this.album, artists: this.album.artist }
    });
  }

  goToEdit() {

  }

  deleteAlbum() {
    if (!this.album?.albumId) return;

    this.dialogType = 'confirmation';
    this.dialogTitle = 'Are you sure?';
    this.dialogMessage = `Do you really want to delete "${this.album.title}"?`;
    this.showDialog = true;
  }
  onDialogClosed(confirmed: boolean) {
    // Simply close the dialog for informational messages
    this.showDialog = false;
  }


  protected readonly UserRole = UserRole;
}
