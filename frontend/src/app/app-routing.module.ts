import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomepageComponent } from './homepage/homepage.component';
import { CreateArtistComponent } from './artists/create-artist/create-artist.component';
import { CreateSongComponent } from './songs/create-song/create-song.component';

const routes: Routes = [
  { path: '', redirectTo: '/home', pathMatch: 'full' },
  { path: 'home', component:HomepageComponent },
  { path: 'create-artist', component:CreateArtistComponent},
  { path: 'create-song', component:CreateSongComponent},
  { path: '**', redirectTo: 'home' },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {}