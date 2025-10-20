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
export class AllArtistsPageComponent implements OnInit, AfterViewInit {
  artists: Artist[] = [];
  displayDots: number[] = [];
  activeIndex = 0;

  scrollAmount = 0;
  intervalId: any;

  @ViewChild('scrollContainer') scrollContainer!: ElementRef<HTMLDivElement>;

  constructor(private service:ArtistService) {}

  ngOnInit(): void {
    // this.service.getAll().subscribe(a=>
    //   {
    //     this.artists = a;
    //     this.updateDots();
    //   });
    this.artists = this.service.getAllMock() // TODO: change to getAll
  }

  ngAfterViewInit() {
    this.intervalId = setInterval(() => this.scrollNext(), 5000);
  }

  scrollNext() {
    if (!this.scrollContainer) return;
    const container = this.scrollContainer.nativeElement;
    const cardWidth = container.firstElementChild?.clientWidth || 200;

    this.scrollAmount += cardWidth + 16;
    if (this.scrollAmount >= container.scrollWidth) {
      this.scrollAmount = 0;
      this.activeIndex = 0;
    } else {
      this.activeIndex = (this.activeIndex + 1) % this.artists.length;
    }

    container.scrollTo({ left: this.scrollAmount, behavior: 'smooth' });
    this.updateDots();
  }

  onScroll() {
    if (!this.scrollContainer) return;
    const container = this.scrollContainer.nativeElement;
    const cardWidth = container.firstElementChild?.clientWidth || 200;
    this.activeIndex = Math.round(container.scrollLeft / (cardWidth + 16)) % this.artists.length;
    this.updateDots();
  }

  updateDots() {
    const total = this.artists.length;
    const active = this.activeIndex;
    const windowSize = 5;
    const dots: number[] = [];

    if (total <= windowSize) {
      for (let i = 0; i < total; i++) dots.push(i);
    } else {
      dots.push(0); // first

      let start = Math.max(active - 1, 1);
      let end = Math.min(active + 1, total - 2);

      for (let i = start; i <= end; i++) {
        if (i !== 0 && i !== total - 1) dots.push(i);
      }

      dots.push(total - 1); // last

      while (dots.length < windowSize) {
        if (dots[1] > 1) {
          dots.splice(1, 0, dots[1] - 1);
        } else if (dots[dots.length - 2] < total - 2) {
          dots.splice(dots.length - 1, 0, dots[dots.length - 2] + 1);
        } else {
          break;
        }
      }
    }

    this.displayDots = dots;
  }

  ngOnDestroy() {
    clearInterval(this.intervalId);
  }
}
