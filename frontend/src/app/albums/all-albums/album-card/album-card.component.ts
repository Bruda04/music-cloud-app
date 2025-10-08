import { Component, Input } from '@angular/core';
import { Album } from '../../model/album.model';
import { Artist } from '../../../artists/model/artist.model';

@Component({
  selector: 'app-album-card',
  templateUrl: './album-card.component.html',
  styleUrls: ['../../../shared/themes/card.css'],
  standalone:false
})
export class AlbumCardComponent {
    @Input() album: Album | undefined; 
    @Input() artists: Artist[] = [];
    
    getArtistNames(): string {
    if (!this.album || !this.album.artistIds?.length) return 'Unknown artist';
        return this.album.artistIds
        .map(id => this.artists.find(a => a.artistId === id)?.name || 'Unknown artist')
        .join(', ');
    }
}
