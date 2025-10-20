import { Component, Input } from '@angular/core';
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
export class AlbumCardComponent {
  @Input() album: Album | undefined;
  @Input() artists: Artist[] = [];
  photoPath: string = 'photo.jpg';


  showDialog = false;
  dialogType: DialogType = 'confirmation';
  dialogTitle = '';
  dialogMessage = '';


  constructor(private router:Router,  protected authService: AuthService){}

  getArtistNames(): string {
  if (!this.album || !this.album.artistIds?.length) return 'Unknown artist';
      return this.album.artistIds
      .map(id => this.artists.find(a => a.artistId === id)?.name || 'Unknown artist')
      .join(', ');
  }

  openAlbum() {
    if (!this.album || !this.album.albumId) {
      console.error('Album ID is missing:', this.album);
      return;
    }
    this.router.navigate(['/albums/details/', this.album.albumId], {
      state: { album: this.album, artists: this.artists }
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
