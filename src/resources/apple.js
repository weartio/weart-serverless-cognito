/**
 * 
 * @param {*} clientId 
 * @param {*} teamId 
 * @param {*} keyId 
 * @param {*} privateKey 
 * @param {*} cognitoUserPoolRef 
 * @param {*} refName 
 * @returns 
 */
function buildAppleIdentityProvider(clientId, teamId, keyId, privateKey, cognitoUserPoolRef, refName = "AppleCognitoUserPoolIdentityProvider") {
  return {
    [refName]: {
      Type: 'AWS::Cognito::UserPoolIdentityProvider',
      Properties: {
        ProviderName: 'SignInWithApple',
        AttributeMapping: {
          email: "email",
        },
        ProviderDetails: {
          client_id: clientId,
          team_id: teamId,
          key_id: keyId,
          private_key: privateKey,
          authorize_scopes: 'email'
        },
        ProviderType: 'SignInWithApple',
        UserPoolId: {
          "Ref": cognitoUserPoolRef
        }
      }
    }
  }
}


module.exports = {
  buildAppleIdentityProvider
}