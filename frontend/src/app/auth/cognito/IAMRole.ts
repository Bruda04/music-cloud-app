import { CognitoIdentityClient, GetIdCommand, GetCredentialsForIdentityCommand } from "@aws-sdk/client-cognito-identity";

export async function getIamRole(idToken: string) {
  const client = new CognitoIdentityClient({ region: 'eu-central-1' });

  const identityIdRes = await client.send(new GetIdCommand({
    IdentityPoolId: 'eu-central-1:f4925b37-1e21-4c9d-b2ab-c11132e693cb',
    Logins: {
      'cognito-idp.eu-central-1.amazonaws.com/eu-central-1_vS3vkgRGf': idToken
    }
  }));

  const creds = await client.send(new GetCredentialsForIdentityCommand({
    IdentityId: identityIdRes.IdentityId,
    Logins: {
      'cognito-idp.eu-central-1.amazonaws.com/eu-central-1_vS3vkgRGf': idToken
    }
  }));

  console.log("IAM Role ARN:", creds.Credentials?.AccessKeyId ? creds.Credentials : "Nema role");
}
