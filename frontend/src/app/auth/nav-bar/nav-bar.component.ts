import { Router } from '@angular/router';
import { Component, inject, signal } from '@angular/core';
import { OidcSecurityService } from 'angular-auth-oidc-client';
import { getIamRole } from '../../auth/cognito/IAMRole';

@Component({
  selector: 'app-navbar',
  templateUrl: './nav-bar.component.html',
  styleUrls: ['./nav-bar.component.css'],
  standalone:false
})
export class NavbarComponent {
    isLoggedIn = false;
    protected readonly title = signal('frontend');
  
    private readonly oidcSecurityService = inject(OidcSecurityService);
    menuOpen = false;

    configuration$ = this.oidcSecurityService.getConfiguration();
    userData$ = this.oidcSecurityService.userData$;


    constructor(private router: Router ) {   
        this.oidcSecurityService.isAuthenticated$.subscribe(({ isAuthenticated }) => {
        this.isLoggedIn = isAuthenticated;
        console.warn('authenticated: ', isAuthenticated);
        this.oidcSecurityService.userData$.subscribe(({ userData }) => {
            console.log('User data:', userData);
            console.log('Groups:', userData['cognito:groups']);
            console.log('Role:', userData['cognito:roles']);
        });
        });
        this.oidcSecurityService.userData$.subscribe(({ userData }) => {
        const idToken = userData.idToken;
        getIamRole(idToken);
        });
    }

    toggleMenu(): void {
        this.menuOpen = !this.menuOpen;
    }

    login(): void {
        this.oidcSecurityService.authorize();
    }

    logout(): void {
        this.oidcSecurityService.logoff().subscribe(result => {
        console.log('logged out', result);
        });
    }
}
