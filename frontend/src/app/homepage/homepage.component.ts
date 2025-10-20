import { Component, OnInit } from '@angular/core';
import { ArtistService } from '../artists/service/artist.service';
import { Artist } from '../artists/model/artist.model';
import { AllArtistsCarouselComponent } from '../artists/all-artists/all-artists-carousel/all-artists.component';
import { AllSongsComponent } from '../songs/all-songs/all-songs.component';
import { AllAlbumsCarouselComponent } from '../albums/all-albums/all-albums-carousel/all-albums.component';
import {NgIf} from '@angular/common';
import {AuthService} from '../auth/auth.service';
import {UserRole} from '../auth/model/user.model';

@Component({
  selector: 'app-root',
  templateUrl: './homepage.component.html',
  styleUrls: ['./homepage.component.css'],
  standalone: true,
  imports: [AllSongsComponent, AllArtistsCarouselComponent, AllAlbumsCarouselComponent, NgIf]
})
export class HomepageComponent implements OnInit{
  artists: Artist[]=[]
  constructor(protected authService: AuthService){}
  ngOnInit(): void {
  }

  protected readonly UserRole = UserRole;
}
