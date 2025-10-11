import { Component, Input } from '@angular/core';
import { Artist } from '../../model/artist.model';

@Component({
  selector: 'app-artist-card',
  templateUrl: './artist-card.component.html',
  styleUrls: ['../../../shared/themes/card.css'],
  standalone:false
})
export class ArtistCardComponent {
  @Input() artist: Artist | undefined; 
}
