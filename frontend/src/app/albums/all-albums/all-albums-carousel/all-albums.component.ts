import { AfterViewInit, Component, ElementRef, Input, OnInit, ViewChild } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Album } from '../../model/album.model';
import { AlbumService } from '../../service/album.service';
import { AlbumsModule } from '../../albums.module';
import { Artist } from '../../../artists/model/artist.model';

@Component({
  selector: 'app-all-albums-carousel',
  templateUrl: './all-albums.component.html',
  styleUrls: ['../../../shared/themes/all-items.css'],
  imports:[AlbumsModule,CommonModule],
  standalone: true
})
export class AllAlbumsCarouselComponent implements OnInit, AfterViewInit {
  @Input() artists: Artist[] = [];
  albums: Album[] = [];
  displayDots: number[] = [];
  activeIndex = 0;

  scrollAmount = 0;
  intervalId: any;

  @ViewChild('scrollContainer') scrollContainer!: ElementRef<HTMLDivElement>;

  constructor(private service:AlbumService) {}

  ngOnInit(): void {
    // this.service.get10New().subscribe(a=>this.albums=a);
    this.albums = this.service.getMock() // TODO: change to get10New
    this.updateDots();
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
      this.activeIndex = (this.activeIndex + 1) % this.albums.length;
    }

    container.scrollTo({ left: this.scrollAmount, behavior: 'smooth' });
    this.updateDots();
  }

  onScroll() {
    if (!this.scrollContainer) return;
    const container = this.scrollContainer.nativeElement;
    const cardWidth = container.firstElementChild?.clientWidth || 200;
    this.activeIndex = Math.round(container.scrollLeft / (cardWidth + 16)) % this.albums.length;
    this.updateDots();
  }

  updateDots() {
    const total = this.albums.length;
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
