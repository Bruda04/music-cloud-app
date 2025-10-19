export const environment = {
  production: false,
  oidc: {
    authority: 'https://cognito-idp.eu-central-1.amazonaws.com/eu-central-1_wdx0LmaLc',
    redirectUrl: 'http://localhost:4200/home',
    clientId: '4c5t0073toj8rnc8vc79t3teds',
    logoutUrl: 'https://cloudmusicapp.auth.eu-central-1.amazoncognito.com/logout?client_id=4c5t0073toj8rnc8vc79t3teds&logout_uri=http://localhost:4200/home',
  },
  apiUrl: 'https://3lkfw4exf0.execute-api.eu-central-1.amazonaws.com/dev'
};
