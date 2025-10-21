import {Component, OnInit} from '@angular/core';
import {FeedService} from './service/feed.service';
import {FeedResponseModel} from './model/feedResponseModel';

@Component({
  selector: 'app-feed',
  templateUrl: './feed.component.html',
  standalone: true,
  styleUrls: ['./feed.component.css', '../shared/themes/card.css']
})
export class FeedComponent implements OnInit {
  protected feedItems: FeedResponseModel = {
    songs: [],
    albums: []
  };

  constructor(private feedService: FeedService) {
  }

  ngOnInit() {
    // this.loadFeed();
    this.loadMockFeed();
  }

  loadFeed() {
    this.feedService.getFeed().subscribe({
      next: (feed: FeedResponseModel) => {
        if (feed) {
          this.feedItems = feed;
          console.log('Feed loaded:', this.feedItems);
        }
      },
      error: (err: any) => {
        console.error('Error unsubscribing from artist:', err);
      }
    });
  }

  loadMockFeed() {}


}
