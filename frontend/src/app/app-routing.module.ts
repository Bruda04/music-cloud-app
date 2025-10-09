import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomepageComponent } from './homepage/homepage.component';
import { CreateArtistComponent } from './artists/create-artist/create-artist.component';
import { CreateSongComponent } from './songs/create-song/create-song.component';
import { CreateAlbumComponent } from './albums/create-album/create-album.component';
import { AllArtistsCarouselComponent } from './artists/all-artists/all-artists-carousel/all-artists.component';
import { AllArtistsPageComponent } from './artists/all-artists/all-artists-page/all-artists.component';
import { AllAlbumsPageComponent } from './albums/all-albums/all-albums-page/all-albums.component';
import { AlbumDetailsComponent } from './albums/details/details.component';

const routes: Routes = [
  { path: '', redirectTo: '/home', pathMatch: 'full' },
  { path: 'home', component:HomepageComponent },
  { path: 'create-artist', component:CreateArtistComponent},
  { path: 'create-song', component:CreateSongComponent},
  { path: 'create-album', component:CreateAlbumComponent},
  { path: 'all-artists', component: AllArtistsPageComponent},
  { path: 'all-albums', component: AllAlbumsPageComponent},
  { path: 'albums/:id', component: AlbumDetailsComponent },
  { path: '**', redirectTo: 'home' },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {}