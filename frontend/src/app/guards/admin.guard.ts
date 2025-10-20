import { Injectable } from '@angular/core';
import { CanActivate, Router } from '@angular/router';
import { NavbarComponent } from '../auth/nav-bar/nav-bar.component';

@Injectable({ providedIn: 'root' })
export class AdminGuard implements CanActivate {
  constructor(private navbar: NavbarComponent, private router: Router) {}

  canActivate(): boolean {
    if (this.navbar.loggedInUser?.role=='Admin') return true;
    this.router.navigate(['/home']);
    return false;
  }
}
