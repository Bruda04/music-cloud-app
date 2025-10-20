export const environment = {
  production: false,
  oidc: {
    authority: 'https://cognito-idp.eu-central-1.amazonaws.com/eu-central-1_oMRl9AAzL',
    redirectUrl: 'http://localhost:4200/home',
    clientId: '3c7lu14e4gopdbb2vsqscrgarc',
    logoutUrl: 'https://cloudmusicapp.auth.eu-central-1.amazoncognito.com/logout?client_id=3c7lu14e4gopdbb2vsqscrgarc&logout_uri=http://localhost:4200/home',
  },
  apiUrl: 'https://r4riagry0h.execute-api.eu-central-1.amazonaws.com/dev'
};
