import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomepageComponent } from './homepage/homepage.component';
import { CreateArtistComponent } from './artists/create-artist/create-artist.component';
import { CreateSongComponent } from './songs/create-song/create-song.component';
import { CreateAlbumComponent } from './albums/create-album/create-album.component';
import { AllArtistsPageComponent } from './artists/all-artists/all-artists-page/all-artists.component';
import { AllAlbumsPageComponent } from './albums/all-albums/all-albums-page/all-albums.component';
import { AlbumDetailsComponent } from './albums/details/details.component';
import { AdminGuard } from './guards/admin.guard';

const routes: Routes = [
  { path: '', redirectTo: '/home', pathMatch: 'full' },
  { path: 'home', component: HomepageComponent },
  { path: 'artists', component: AllArtistsPageComponent},
  { path: 'artists/create', component: CreateArtistComponent, canActivate: [AdminGuard]},
  { path: 'albums', component: AllAlbumsPageComponent},
  { path: 'albums/details/:id', component: AlbumDetailsComponent },
  { path: 'albums/create', component: CreateAlbumComponent, canActivate: [AdminGuard]},
  { path: 'songs/create', component: CreateSongComponent, canActivate: [AdminGuard]},
  { path: 'songs/edit/:id', component: CreateSongComponent },
  { path: '**', redirectTo: 'home' },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {}