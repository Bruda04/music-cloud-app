import { AfterViewInit, Component, ElementRef, Input, OnInit, ViewChild } from '@angular/core';
import { Artist } from '../../model/artist.model';
import { ArtistService } from '../../service/artist.service';
import { ArtistsModule } from '../../artists.module';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-all-artists-page',
  templateUrl: './all-artists.component.html',
  styleUrls: ['../../../shared/themes/all-items.css'],
  imports:[ArtistsModule,CommonModule],
  standalone: true
})
export class AllArtistsPageComponent implements OnInit {
  artists: Artist[] = [];
  lastKey?: string;
  limit = 6;
  page = 1;

  constructor(private service:ArtistService) {}

  ngOnInit(): void {
    this.loadArtists()
  }

  loadArtists(lastKey?: string){
    this.service.getAll(this.limit, lastKey).subscribe(res=>
    {
      this.artists = res.artists;
      this.lastKey = res.lastKey;
    });
  }

  nextPage() {
    if (this.lastKey) {
      this.page++;
      this.loadArtists(this.lastKey);
    }
  }

  prevPage() {
    if (this.page > 1) {
      this.page--;
      this.loadArtists();
    }
  }

}
