import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { DiscoveryComponent } from './discovery.component';
import { ArtistsModule } from '../artists/artists.module';
import { AlbumsModule } from '../albums/albums.module';
import {DialogComponent} from '../shared/dialog/dialog.component';

@NgModule({
  declarations: [DiscoveryComponent], // now it's declared
  imports: [
    CommonModule,
    ArtistsModule, // provides <app-artist-card>
    AlbumsModule,
    DialogComponent,
    // provides <app-album-card>
  ],
  exports: [DiscoveryComponent]
})
export class DiscoveryModule {}
