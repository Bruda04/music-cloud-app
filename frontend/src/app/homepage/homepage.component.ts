import { Component, inject, signal } from '@angular/core';
import { OidcSecurityService } from 'angular-auth-oidc-client';
import { CommonModule } from '@angular/common';
import { getIamRole } from '../auth/cognito/IAMRole';

@Component({
  selector: 'app-root',
  imports: [CommonModule],
  templateUrl: './homepage.component.html',
  styleUrls: []
})
export class HomepageComponent {
  ngOnInit(): void {
    
  }
}
