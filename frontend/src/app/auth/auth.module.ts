import {AuthModule} from 'angular-auth-oidc-client';
import { NgModule } from '@angular/core';

@NgModule({
  imports: [
    AuthModule.forRoot({
      config: {
        authority: 'https://cognito-idp.eu-central-1.amazonaws.com/eu-central-1_vS3vkgRGf',
        redirectUrl: 'http://localhost:4200/home',
        clientId: '2benlt2a56e7ua5f08m1s41qnu',
        scope: 'email openid phone',
        responseType: 'code'
      },
    }),
  ],
  exports: [AuthModule],
})
export class AppAuthModule {}
