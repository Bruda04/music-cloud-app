import {AuthModule} from 'angular-auth-oidc-client';
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import {environment} from '../environment/environment';

@NgModule({
  imports: [
    AuthModule.forRoot({
      config: {
        authority: environment.oidc.authority,
        redirectUrl: environment.oidc.redirectUrl,
        clientId: environment.oidc.clientId,
        scope: 'email openid profile',
        responseType: 'code'
      },
    }),
    CommonModule,
    FormsModule,
  ],
  exports: [AuthModule],
})
export class AppAuthModule {}
