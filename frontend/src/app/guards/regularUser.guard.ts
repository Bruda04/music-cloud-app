import {Injectable} from '@angular/core';
import {CanActivate, Router} from '@angular/router';
import {AuthService} from '../auth/auth.service';
import {UserRole} from '../auth/model/user.model';

@Injectable({ providedIn: 'root' })
export class RegularUserGuard implements CanActivate {
  constructor(private authService: AuthService, private router: Router) {}

  canActivate(): boolean {
    console.log(this.authService.loggedInUser)
    if (this.authService.loggedInUser?.role==UserRole.AuthUser) return true;
    this.router.navigate(['/home']);
    return false;
  }
}
