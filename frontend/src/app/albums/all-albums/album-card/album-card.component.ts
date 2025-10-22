import {Component, EventEmitter, Input, OnInit, Output} from '@angular/core';
import { Album } from '../../model/album.model';
import { Artist } from '../../../artists/model/artist.model';
import { Router } from '@angular/router';
import {UserRole} from '../../../auth/model/user.model';
import {AuthService} from '../../../auth/auth.service';
import {DialogType} from '../../../shared/dialog/dialog.component';
import {CommonModule} from '@angular/common';
import {ImagesService} from '../../../shared/images/service/images.service';
import {AlbumService} from '../../service/album.service';

@Component({
  selector: 'app-album-card',
  templateUrl: './album-card.component.html',
  standalone: false,
  styleUrls: ['../../../shared/themes/card.css']
})
export class AlbumCardComponent implements OnInit {
  @Input() album: Album | undefined;
  photoPath: string | undefined = "photo.png";

  pendingDeleteId: string | null = null;

  showDialog = false;
  dialogType: DialogType = 'confirmation';
  dialogTitle = '';
  dialogMessage = '';
  @Output() deleted = new EventEmitter<string>();



  constructor(private router:Router, private albumService: AlbumService, protected authService: AuthService, private imageService: ImagesService){}

  ngOnInit() {
    this.loadImage();
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
    this.pendingDeleteId = this.album.albumId;

    this.dialogType = 'confirmation';
    this.dialogTitle = 'Are you sure?';
    this.dialogMessage = `Do you really want to delete "${this.album.title}"?`;
    this.showDialog = true;
  }

  onDialogClosed(confirmed: boolean) {
    this.showDialog = false;

    if (confirmed && this.pendingDeleteId) {
      console.log(this.pendingDeleteId)
      this.albumService.delete(this.pendingDeleteId).subscribe({
        next: res => {
          this.dialogType = 'message';
          this.dialogTitle = 'Deleted';
          this.dialogMessage = "Successfully deleted " + this.album?.title;
          this.showDialog = true;
          setTimeout(() => {
            this.deleted.emit(this.pendingDeleteId!);
          }, 5500);
        },
        error: (err) => {
          this.dialogType = 'error';
          this.dialogTitle = 'Error';
          this.dialogMessage = err.error?.message || 'Failed to delete album';
          this.showDialog = true;
        }
      });
    }
  }


  protected readonly UserRole = UserRole;

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
}
