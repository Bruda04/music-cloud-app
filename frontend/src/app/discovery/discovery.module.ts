import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { DiscoveryComponent } from './discovery.component';
import { ArtistsModule } from '../artists/artists.module';
import { AlbumsModule } from '../albums/albums.module';

@NgModule({
  declarations: [DiscoveryComponent], // now it's declared
  imports: [
    CommonModule,
    ArtistsModule, // provides <app-artist-card>
    AlbumsModule   // provides <app-album-card>
  ],
  exports: [DiscoveryComponent]
})
export class DiscoveryModule {}
