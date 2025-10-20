import {Injectable} from '@angular/core';
import {CanActivate, Router} from '@angular/router';
import {AuthService} from '../auth/auth.service';
import {UserRole} from '../auth/model/user.model';

@Injectable({ providedIn: 'root' })
export class AdminGuard implements CanActivate {
  constructor(private authService: AuthService, private router: Router) {}

  canActivate(): boolean {
    if (this.authService.loggedInUser?.role==UserRole.Admin) return true;
    this.router.navigate(['/home']);
    return false;
  }
}
