import { Component, OnInit } from '@angular/core';
import { Artist } from '../artists/model/artist.model';
import {NgIf} from '@angular/common';
import {AuthService} from '../auth/auth.service';
import {UserRole} from '../auth/model/user.model';
import {FeedComponent} from '../feed/feed.component';

@Component({
  selector: 'app-root',
  templateUrl: './homepage.component.html',
  styleUrls: ['./homepage.component.css'],
  standalone: true,
  imports: [NgIf, FeedComponent]
})
export class HomepageComponent implements OnInit{
  artists: Artist[]=[]
  constructor(protected authService: AuthService,
  ){}

  ngOnInit(): void {
  }



  protected readonly UserRole = UserRole;
}
