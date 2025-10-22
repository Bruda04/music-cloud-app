import { Component, HostListener, OnInit } from '@angular/core';
import { AuthService } from '../auth/auth.service';
import {Artist} from '../artists/model/artist.model';
import {Album} from '../albums/model/album.model';
import {DialogComponent, DialogType} from '../shared/dialog/dialog.component';
import {SubscriptionService} from '../subscriptions/service/subscription.service';
import {SongService} from '../songs/service/song.service';
import {GenreService} from '../songs/service/genre.service';
import {NgForOf, NgIf} from '@angular/common';
import {ArtistsModule} from '../artists/artists.module';
import {AlbumsModule} from '../albums/albums.module';

interface Genre { name: string; }

@Component({
  selector: 'app-discovery',
  templateUrl: './discovery.component.html',
  standalone: true,
  imports: [
    NgForOf,
    ArtistsModule,
    NgIf,
    AlbumsModule,
    DialogComponent
  ],
  styleUrls: ['./discovery.component.scss', '../shared/themes/card.css']
})
export class DiscoveryComponent implements OnInit {
  genres: Genre[] = [];

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

  constructor(protected authService: AuthService, private subscriptionService: SubscriptionService, private genreService: GenreService) {}

  ngOnInit(): void {
    setTimeout(() => this.updateActiveDot(), 0);
    this.loadGenres()
  }

  selectGenre(genre: Genre) {
    this.selectedGenre = genre;
    this.loadDataForGenre(genre);
  }

  subscribeToGenre(genre: Genre, event: MouseEvent) {
    if (!genre) return;
    event.stopPropagation();
    // this.subscriptionService.subscribeToGenre(genre.name).subscribe({
    //   next: () => {
    //     this.dialogTitle = 'Subscribed';
    //     this.dialogMessage = `You have subscribed to the genre: ${genre.name}.`;
    //     this.dialogType = 'message';
    //     this.showDialog = true;
    //   },
    //   error: (err) => {
    //     console.error('Error subscribing to genre:', err);
    //     this.dialogTitle = 'Error';
    //     this.dialogMessage = `Failed to subscribe to genre: ${genre.name}. Please try again later.`;
    //     this.dialogType = 'message';
    //     this.showDialog = true;
    //   }
    // });
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

  private loadGenres() {
    this.genreService.getAll().subscribe({
      next: (genres) => {
        this.genres = genres.map(g => ({ name: g.genreName }));
      },
      error: (err) => {
        console.error('Error loading genres:', err);
      }
    });
  }

  private loadDataForGenre(genre: Genre) {
    this.genreService.getContentByGenre(genre.name).subscribe({
      next: (data) => {
        this.albumsAndArtistsForGenre = {
          artists: data.artists,
          albums: data.albums
        };
      },
      error: (err) => {
        console.error(`Error loading data for genre ${genre.name}:`, err);
      }
    });
  }
}
