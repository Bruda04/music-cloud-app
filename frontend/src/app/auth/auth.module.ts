import {AuthModule} from 'angular-auth-oidc-client';
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { BrowserModule } from '@angular/platform-browser';

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
    CommonModule,
    FormsModule,
    BrowserModule
  ],
  exports: [AuthModule],
})
export class AppAuthModule {}
