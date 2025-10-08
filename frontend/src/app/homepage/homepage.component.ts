import { Component, OnInit } from '@angular/core';
import { ArtistService } from '../artists/service/artist.service';
import { Artist } from '../artists/model/artist.model';
import { AllArtistsComponent } from '../artists/all-artists/all-artists.component';
import { AllSongsComponent } from '../songs/all-songs/all-songs.component';

@Component({
  selector: 'app-root',
  templateUrl: './homepage.component.html',
  styleUrls: ['./homepage.component.css'],
  standalone: true,
  imports: [AllSongsComponent,AllArtistsComponent]
})
export class HomepageComponent implements OnInit{
  artists: Artist[]=[]
  constructor(private artistService:ArtistService){}
  ngOnInit(): void {
    // this.service.getAll().subscribe(a=>{
    //   this.artists = a;
    // });
    this.artists = this.artistService.getAllMock(); // TODO: change to getAll, its like this so i dont use all aws free requests
  }
}
