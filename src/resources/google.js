/**
 * 
 * @param {*} clientId 
 * @param {*} clientSecret 
 * @param {*} cognitoUserPoolRef 
 * @returns 
 */
function buildGoogleIdentityProvider(clientId, clientSecret, cognitoUserPoolRef, refName = "GoogleCognitoUserPoolIdentityProvider") {
  return {
    [refName]: {
      Type: 'AWS::Cognito::UserPoolIdentityProvider',
      Properties: {
        ProviderName: 'Google',
        AttributeMapping: {
          email: "email",
          email_verified: "email_verified",
          picture: "picture",
          "custom:access_token": "access_token",
        },
        ProviderDetails: {
          client_id: clientId,
          client_secret: clientSecret,
          authorize_scopes: 'profile email openid'
        },
        ProviderType: 'Google',
        UserPoolId: {
          "Ref": cognitoUserPoolRef
        }
      }
    }
  }
}

module.exports = {
  buildGoogleIdentityProvider
}