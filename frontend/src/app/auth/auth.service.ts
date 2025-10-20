import { Injectable, inject } from '@angular/core';
import { OidcSecurityService } from 'angular-auth-oidc-client';
import { BehaviorSubject } from 'rxjs';
import { environment } from '../environment/environment';
import { UserModel, UserRole } from './model/user.model';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private oidcSecurityService = inject(OidcSecurityService);

  private userSubject = new BehaviorSubject<UserModel | null>(null);
  user$ = this.userSubject.asObservable();

  get loggedInUser(): UserModel | null {
    return this.userSubject.value;
  }

  constructor() {
    this.oidcSecurityService.checkAuth().subscribe(({ isAuthenticated, userData, idToken }) => {
      if (isAuthenticated && idToken) {
        this.handleLogin(idToken, userData);
      } else {
        this.userSubject.next(null);
        localStorage.removeItem('jwt');
      }
    });

    this.oidcSecurityService.isAuthenticated$.subscribe(({ isAuthenticated }) => {
      if (!isAuthenticated) {
        this.userSubject.next(null);
        localStorage.removeItem('jwt');
      }
    });
  }

  login(): void {
    this.oidcSecurityService.authorize();
  }

  logout(): void {
    window.sessionStorage.clear();
    localStorage.clear();

    window.location.href = environment.oidc.logoutUrl;
  }

  private handleLogin(idToken: string, userData?: any) {
    const payload = this.decodeJwt(idToken);
    const group = payload['cognito:groups']?.[0];
    let role: UserRole;

    switch (group) {
      case 'Admins':
        role = UserRole.Admin;
        break;
      case 'AuthUsers':
        role = UserRole.AuthUser;
        break;
      default:
        role = UserRole.AuthUser;
    }

    const user: UserModel = {
      userId: payload['sub'],
      email: payload['email'],
      role: role
    };

    this.userSubject.next(user);
    localStorage.setItem('jwt', idToken);
    console.log('Logged in user:', user);
  }

  private decodeJwt(token: string): any {
    try {
      const payload = token.split('.')[1];
      return JSON.parse(atob(payload));
    } catch (e) {
      console.error('Invalid JWT token:', e);
      return {};
    }
  }
}
