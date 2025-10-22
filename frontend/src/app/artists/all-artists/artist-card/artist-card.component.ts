import { Component, Input } from '@angular/core';
import { Artist } from '../../model/artist.model';
import {UserRole} from '../../../auth/model/user.model';
import {DialogType} from '../../../shared/dialog/dialog.component';
import {AuthService} from '../../../auth/auth.service';
import {Router} from '@angular/router';
import { ArtistService } from '../../service/artist.service';

@Component({
  selector: 'app-artist-card',
  standalone: false,
  templateUrl: './artist-card.component.html',
  styleUrls: ['../../../shared/themes/card.css']
})
export class ArtistCardComponent {
  @Input() artist: Artist | undefined;
  protected readonly userRole?: UserRole;

  showDialog: boolean = false;
  dialogType: DialogType = 'message';
  dialogTitle: string = '';
  dialogMessage: string = '';

  constructor(private router:Router,  protected authService: AuthService, private artistServie: ArtistService){
    this.userRole = this.authService.loggedInUser?.role;
  }

  subscribeToArtist(): void {
    if (!this.artist) return;

    // Show success dialog
    this.dialogType = 'message';
    this.dialogTitle = 'Subscribed!';
    this.dialogMessage = `Successfully subscribed to ${this.artist.name}.`;
    this.showDialog = true;
  }

  onDialogClosed(confirmed: boolean) {
    this.showDialog = false;
  }

  openArtistSongs() {
    if (!this.artist || !this.artist.artistId) {
      console.error('Artist ID is missing:', this.artist);
      return;
    }
    this.router.navigate(['/artists/details/', this.artist.artistId], {
      state: { artist: this.artist }
    });
  }
  
  delete(event: MouseEvent): void {
    event.stopPropagation(); 
    if (!this.artist || !this.artist.artistId) {
      console.error('Artist ID is missing:', this.artist);
      return;
    } 

    this.artistServie.delete(this.artist.artistId).subscribe({
      next: () => {
        this.dialogType = 'message';
        this.dialogTitle = 'Deleted!';
        this.dialogMessage = `Successfully deleted ${this.artist?.name}.`;
        this.showDialog = true;
      },
      error: (err) => {
        console.error(err);
        this.dialogType = 'error';
        this.dialogTitle = 'Error';
        this.dialogMessage = `Failed to delete ${this.artist?.name}. Please try again later.`;
        this.showDialog = true;
      }
    });
  }

}
