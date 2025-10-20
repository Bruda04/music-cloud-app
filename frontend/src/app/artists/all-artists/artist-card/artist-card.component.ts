import { Component, Input } from '@angular/core';
import { Artist } from '../../model/artist.model';
import {UserRole} from '../../../auth/model/user.model';
import {DialogType} from '../../../shared/dialog/dialog.component';
import {AuthService} from '../../../auth/auth.service';

@Component({
  selector: 'app-artist-card',
  standalone: false,
  templateUrl: './artist-card.component.html',
  styleUrls: ['../../../shared/themes/card.css']
})
export class ArtistCardComponent {
  @Input() artist: Artist | undefined;
  protected readonly UserRole = UserRole;

  showDialog: boolean = false;
  dialogType: DialogType = 'message';
  dialogTitle: string = '';
  dialogMessage: string = '';

  subscribeToArtist(): void {
    if (!this.artist) return;

    // Your subscription logic here (service call, etc.)

    // Show success dialog
    this.dialogType = 'message';
    this.dialogTitle = 'Subscribed!';
    this.dialogMessage = `Successfully subscribed to ${this.artist.name}.`;
    this.showDialog = true;
  }

  onDialogClosed(confirmed: boolean) {
    // Simply close the dialog for informational messages
    this.showDialog = false;
  }


}
