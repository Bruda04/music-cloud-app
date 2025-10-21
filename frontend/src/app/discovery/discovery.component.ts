import { Component, HostListener, OnInit } from '@angular/core';
import { AuthService } from '../auth/auth.service';
import {Artist} from '../artists/model/artist.model';
import {Album} from '../albums/model/album.model';
import {DialogType} from '../shared/dialog/dialog.component';

interface Genre { name: string; }

@Component({
  selector: 'app-discovery',
  standalone: false,
  templateUrl: './discovery.component.html',
  styleUrls: ['./discovery.component.scss', '../shared/themes/card.css']
})
export class DiscoveryComponent implements OnInit {
  genres: Genre[] = [
    { name: 'Pop' },
    { name: 'Rock' },
    { name: 'Jazz' },
    { name: 'Classical' },
    { name: 'Hip-Hop' },
    { name: 'Electronic' },
    { name: 'Folk' },
    { name: 'R&B' }
  ];

  showDialog: boolean = false;
  dialogType: DialogType = 'message';
  dialogTitle: string = '';
  dialogMessage: string = '';

  selectedGenre: Genre | null = null;
  albumsAndArtistsForGenre: { artists: Artist[]; albums: Album[] } = { artists: [], albums: [] };
  activeDot = 0;

  private allData: {
    [key: string]: { artists: Artist[]; albums: Album[] };
  } = {
    "Pop": {
      artists: [
        { name: 'Luna', bio: 'Pop sensation', genres: ['Pop'] },
        { name: 'Maya', bio: 'Pop-R&B hybrid', genres: ['Pop', 'R&B'] }
      ],
      albums: [

      ]
    },
    "Rock": {
      artists: [{ name: 'The Waves', bio: 'Rock legends', genres: ['Rock'] }],
      albums: [

      ]
    }
  };

  constructor(protected authService: AuthService) {}

  ngOnInit(): void {
    this.selectGenre(this.genres[0]);
    setTimeout(() => this.updateActiveDot(), 0);
  }

  selectGenre(genre: Genre) {
    this.selectedGenre = genre;
    const data = this.allData[genre.name] || { artists: [], albums: [] };
    this.albumsAndArtistsForGenre = data;
  }

  subscribeToGenre(genre: Genre, event: MouseEvent) {
    if (!genre) return;


    this.dialogType = 'message';
    this.dialogTitle = 'Subscribed!';
    this.dialogMessage = `Successfully subscribed to ${genre.name}.`;
    this.showDialog = true;
  }

  scrollGenres(direction: number) {
    const list = document.querySelector('.horizontal-list') as HTMLElement | null;
    if (!list) return;
    const scrollAmount = 250;
    list.scrollBy({ left: direction * scrollAmount, behavior: 'smooth' });
    this.updateActiveDot();
  }

  @HostListener('window:resize')
  updateActiveDot() {
    const list = document.querySelector('.horizontal-list') as HTMLElement | null;
    if (!list) return;
    const children = Array.from(list.children) as HTMLElement[];
    const scrollLeft = list.scrollLeft;
    let best = 0;
    let bestDiff = Infinity;
    children.forEach((c, i) => {
      const diff = Math.abs(c.offsetLeft - scrollLeft);
      if (diff < bestDiff) {
        bestDiff = diff;
        best = i;
      }
    });
    this.activeDot = best;
  }

  onDialogClosed(confirmed: boolean) {
    // Simply close the dialog for informational messages
    this.showDialog = false;
  }

}
