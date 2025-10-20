import {Router} from '@angular/router';
import {Component, inject, signal} from '@angular/core';
import {OidcSecurityService} from 'angular-auth-oidc-client';
import {UserModel, UserRole} from '../../artists/model/user.model';
import {environment} from '../../environment/environment';

@Component({
  selector: 'app-navbar',
  templateUrl: './nav-bar.component.html',
  styleUrls: ['./nav-bar.component.css'],
  standalone:false
})
export class NavbarComponent {
    isLoggedIn = false;
    protected readonly title = signal('frontend');
    loggedInUser: UserModel | null = null;

    private readonly oidcSecurityService = inject(OidcSecurityService);
    menuOpen = false;

    configuration$ = this.oidcSecurityService.getConfiguration();
    userData$ = this.oidcSecurityService.userData$;

    constructor() {
        this.oidcSecurityService.isAuthenticated$.subscribe(({ isAuthenticated }) => {
        this.isLoggedIn = isAuthenticated;
        console.warn('authenticated: ', isAuthenticated);
        if (isAuthenticated) {
          this.oidcSecurityService.getIdToken().subscribe(idToken => {
            console.log('ID Token:', idToken);
            if (idToken) {
              const payload = this.decodeJwt(idToken);
              const group = payload['cognito:groups']?.[0];
              console.log('User group from token:', group);
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

              this.loggedInUser = {
                userId: payload['sub'],
                email: payload['email'],
                role: role,
              };
              console.log('Decoded JWT payload:', payload);
              console.log('Groups:', payload['cognito:groups']);
              console.log('Logged in user:', this.loggedInUser);
            }
          });
        }
        });
    }

    toggleMenu(): void {
        this.menuOpen = !this.menuOpen;
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
