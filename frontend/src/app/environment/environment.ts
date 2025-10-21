export const environment = {
  production: false,
  oidc: {
    authority: 'https://cognito-idp.eu-central-1.amazonaws.com/eu-central-1_byL11guTB',
    redirectUrl: 'http://localhost:4200/home',
    clientId: '3jsv5prvcumcami95fbajkvico',
    logoutUrl: 'https://cloudmusicapp.auth.eu-central-1.amazoncognito.com/logout?client_id=3jsv5prvcumcami95fbajkvico&logout_uri=http://localhost:4200/home',
  },
  apiUrl: 'https://q2fyxa1q8g.execute-api.eu-central-1.amazonaws.com/dev/'
};
