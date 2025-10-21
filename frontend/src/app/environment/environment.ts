export const environment = {
  production: false,
  oidc: {
    authority: 'https://cognito-idp.eu-central-1.amazonaws.com/eu-central-1_fZa6nkTm2',
    redirectUrl: 'http://localhost:4200/home',
    clientId: '7jhcsh6fia0125035e4chc1gc',
    logoutUrl: 'https://cloudmusicapp.auth.eu-central-1.amazoncognito.com/logout?client_id=7jhcsh6fia0125035e4chc1gc&logout_uri=http://localhost:4200/home',
  },
  apiUrl: 'https://g945mglyn5.execute-api.eu-central-1.amazonaws.com/dev'
};
