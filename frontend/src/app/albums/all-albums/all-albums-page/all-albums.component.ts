import { AfterViewInit, Component, ElementRef, Input, OnInit, ViewChild } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AlbumsModule } from '../../albums.module';
import { Album } from '../../model/album.model';
import { AlbumService } from '../../service/album.service';
import { ArtistService } from '../../../artists/service/artist.service';
import { Artist } from '../../../artists/model/artist.model';

@Component({
  selector: 'app-all-albums-page',
  templateUrl: './all-albums.component.html',
  styleUrls: ['../../../shared/themes/all-items.css'],
  imports:[AlbumsModule,CommonModule],
  standalone: true
})
export class AllAlbumsPageComponent implements OnInit {

    albums: Album[] = [];
    lastKey?: string;
    limit = 6;
    page = 1;

    constructor(private albumService:AlbumService, private artistService: ArtistService) {}

    ngOnInit(): void {
      this.loadAlbums()
    }

    loadAlbums(lastKey?: string){
      this.albumService.getAll(this.limit, lastKey).subscribe(res=>
      {
        this.albums = res.albums;
        this.lastKey = res.lastKey;
      });
    }


    nextPage() {
      if (this.lastKey) {
        this.page++;
        this.loadAlbums(this.lastKey);
      }
    }

    prevPage() {
      if (this.page > 1) {
        this.page--;
        this.loadAlbums();
      }
    }

}
