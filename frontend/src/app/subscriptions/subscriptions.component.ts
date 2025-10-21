import { Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { SubscriptionService } from './service/subscription.service';
import { SubscriptionResponse } from './model/subscriptions.model';
import {DialogComponent, DialogType} from '../shared/dialog/dialog.component';
import {NgForOf, NgIf} from '@angular/common';

@Component({
  selector: 'app-subscriptions',
  templateUrl: './subscriptions.component.html',
  styleUrls: ['./subscriptions.component.css', '../shared/themes/card.css'],
  standalone: true,
  imports: [DialogComponent, NgIf, NgForOf]
})
export class SubscriptionsComponent implements OnInit {

  protected subscriptions: SubscriptionResponse | null = null;

  showDialog = false;
  dialogType: DialogType = 'message';
  dialogTitle = '';
  dialogMessage = '';

  constructor(private subscriptionService: SubscriptionService) {}

  ngOnInit(): void {
    // this.loadSubscriptions();
    this.locdMockSubscriptions();
  }

  private locdMockSubscriptions(): void {
    this.subscriptions = {
      genres: [
        'Rock', 'Pop', 'Jazz', 'Classical',
        'Rock', 'Pop', 'Jazz', 'Classical',
        'Rock', 'Pop', 'Jazz', 'Classical',
        'Rock', 'Pop', 'Jazz', 'Classical',
        'Rock', 'Pop', 'Jazz', 'Classical',
        'Hip-Hop', 'Electronic', 'Country'
      ],
      artists: [
        { artistId: '1', name: 'Artist One' },
        { artistId: '1', name: 'Artist One' },
        { artistId: '1', name: 'Artist One' },
        { artistId: '1', name: 'Artist One' },
        { artistId: '1', name: 'Artist One' },
        { artistId: '2', name: 'Artist Two' },
        { artistId: '3', name: 'Artist Three' }
      ]
    };
  }

  private loadSubscriptions(): void {
    this.subscriptionService.getMySubscriptions().subscribe({
        next: (response: SubscriptionResponse) => {
          console.log('Subscriptions fetched:', response);
          this.subscriptions = response;
        },
        error: (err) => {
          console.error('Error fetching subscriptions:', err);
        }
      });
  }



  unsubscribeFromGenre(genre: string, event: MouseEvent): void {
    event.stopPropagation();
    this.dialogTitle = 'Unsubscribed';
    this.dialogMessage = `You have unsubscribed from ${genre}.`;
    this.showDialog = true;

    this.subscriptionService.unsubscribeFromGenre(genre).subscribe({
      next: () => {
        if (this.subscriptions) {
          this.subscriptions.genres = this.subscriptions.genres.filter(g => g !== genre);
        }
      },
      error: (err: any) => {
        console.error('Error unsubscribing from genre:', err);
      }
    });
  }

  unsubscribeFromArtist(artist: { artistId: string; name: string }): void {
    this.dialogTitle = 'Unsubscribed';
    this.dialogMessage = `You have unsubscribed from ${artist.name}.`;
    this.showDialog = true;

    this.subscriptionService.unsubscribeFromArtist(artist.artistId).subscribe({
      next: () => {
        if (this.subscriptions) {
          this.subscriptions.artists = this.subscriptions.artists.filter(a => a.artistId !== artist.artistId);
        }
      },
      error: (err: any) => {
        console.error('Error unsubscribing from artist:', err);
      }
    });
  }

  onDialogClosed($event: boolean): void {
    this.showDialog = false;
  }

@ViewChild('genreList', { static: false }) genreList!: ElementRef<HTMLDivElement>;

  scrollGenres(direction: number): void {
    if (!this.genreList) return;
    const listEl = this.genreList.nativeElement;
    const scrollAmount = listEl.clientWidth * 0.7;
    listEl.scrollBy({ left: scrollAmount * direction, behavior: 'smooth' });
  }
}
