import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ArtistsModule } from '../artists/artists.module';

@Component({
  selector: 'app-root',
  imports: [CommonModule, ArtistsModule],
  templateUrl: './homepage.component.html',
  styleUrls: ['./homepage.component.css']
})
export class HomepageComponent {
  ngOnInit(): void {
  }
}
