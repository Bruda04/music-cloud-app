import { Component, signal } from '@angular/core';
import { AuthService } from '../auth.service';
import { UserModel } from '../model/user.model';

@Component({
  selector: 'app-navbar',
  templateUrl: './nav-bar.component.html',
  styleUrls: ['./nav-bar.component.css'],
  standalone: false
})
export class NavbarComponent {
  protected readonly title = signal('frontend');
  menuOpen = false;

  isLoggedIn = false;
  loggedInUser: UserModel | null = null;

  constructor(private authService: AuthService) {
    this.authService.user$.subscribe(user => {
      this.loggedInUser = user;
      this.isLoggedIn = !!user;
    });
  }

  toggleMenu(): void {
    this.menuOpen = !this.menuOpen;
  }

  login(): void {
    this.authService.login();
  }

  logout(): void {
    this.authService.logout();
  }
}
