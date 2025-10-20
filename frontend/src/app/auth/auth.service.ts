import { Injectable, inject } from '@angular/core';
import { OidcSecurityService } from 'angular-auth-oidc-client';
import { BehaviorSubject } from 'rxjs';
import { UserModel, UserRole } from '../artists/model/user.model';
import { environment } from '../environment/environment';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private oidcSecurityService = inject(OidcSecurityService);

  // Observable za trenutno ulogovanog korisnika
  private userSubject = new BehaviorSubject<UserModel | null>(null);
  user$ = this.userSubject.asObservable();

  // Trenutno stanje korisnika (sinhrono)
  get loggedInUser(): UserModel | null {
    return this.userSubject.value;
  }

  constructor() {
    this.oidcSecurityService.isAuthenticated$.subscribe(({ isAuthenticated }) => {
      if (isAuthenticated) {
        this.oidcSecurityService.getIdToken().subscribe(idToken => {
          if (idToken) {
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
              role: role,
            };

            console.log('Decoded JWT payload:', payload);
            console.log('Groups:', payload['cognito:groups']);
            console.log('Logged in user:', user);

            this.userSubject.next(user);
          }
        });
      } else {
        this.userSubject.next(null);
      }
    });
  }

  login(): void {
    this.oidcSecurityService.authorize();
  }

  logout(): void {
    if (window.sessionStorage) {
      window.sessionStorage.clear();
    }
    window.location.href = environment.oidc.logoutUrl;
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
