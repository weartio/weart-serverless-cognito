const { isEmpty } = require("./uilts")

/**
 * 
 * @param {*} googleRef 
 * @param {*} appleRef 
 * @param {*} CognitoUserPoolRef 
 * @param {*} loginCallbackUrl 
 * @param {*} logoutCallbackUrl 
 * @param {*} refName 
 * @returns 
 */
function buildUserPoolClient(rcsPrefix, googleRef, appleRef, CognitoUserPoolRef = "CognitoUserPool",
    loginCallbackUrl = "", logoutCallbackUrl = "", refName = "CognitoUserPoolClient") {
    return {
        [refName]: {
            "Type": "AWS::Cognito::UserPoolClient",
            "DeletionPolicy": "Delete",
            "Properties": {
                "ClientName": `${rcsPrefix}-users-client`,
                "AllowedOAuthFlows": [
                    "code"
                ],
                "AllowedOAuthFlowsUserPoolClient": true,
                "AllowedOAuthScopes": [
                    "email",
                    "openid",
                    "aws.cognito.signin.user.admin",
                    "profile"
                ],
                "ExplicitAuthFlows": [
                    "ALLOW_ADMIN_USER_PASSWORD_AUTH",
                    "ALLOW_CUSTOM_AUTH",
                    "ALLOW_USER_SRP_AUTH",
                    "ALLOW_REFRESH_TOKEN_AUTH"
                ],
                "SupportedIdentityProviders": [
                    "COGNITO",
                    ...!isEmpty(googleRef) ? ["Google"] : [],
                    ...!isEmpty(appleRef) ? ["SignInWithApple"] : [],
                ],
                "CallbackURLs": [
                    loginCallbackUrl
                ],
                "LogoutURLs": [
                    logoutCallbackUrl
                ],
                "UserPoolId": {
                    "Ref": CognitoUserPoolRef
                }
            },
            ...!isEmpty(googleRef) ? {
                "DependsOn": [
                    googleRef.ref
                ]
            } : {}
        }
    }
}

module.exports = {
    buildUserPoolClient
}