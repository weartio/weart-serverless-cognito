const { getResourceArn } = require("./uilts");


function buildCognitoIdentityPoolRoleAttachment(IdentityPoolIdRef, cognitoAuthRoleRef, cognitoUnauthRoleRef, refName = "CognitoIdentityPoolRoles") {
    return {
        [refName]: {
            "Type": "AWS::Cognito::IdentityPoolRoleAttachment",
            "DeletionPolicy": "Delete",
            "Properties": {
                "IdentityPoolId": {
                    "Ref": IdentityPoolIdRef
                },
                "Roles": {
                    ...getResourceArn("authenticated", cognitoAuthRoleRef),
                    ...getResourceArn("unauthenticated", cognitoUnauthRoleRef),
                }
            }
        },
    }
}

/**
 * 
 * @param {*} cognitoUserPoolRef 
 * @param {*} cognitoUserPoolClientRef 
 * @returns 
 */
function buildIdentityPool(rcsPrefix, cognitoUserPoolRef, cognitoUserPoolClientRef, deleletionPolicy = "Delete", refName = "CognitoIdentityPool") {
    return {
        [refName]: {
            "Type": "AWS::Cognito::IdentityPool",
            "DeletionPolicy": deleletionPolicy,
            "Properties": {
                "IdentityPoolName": `${rcsPrefix}-identity_pool`,
                "AllowUnauthenticatedIdentities": true,
                "CognitoIdentityProviders": [
                    {
                        "ClientId": {
                            "Ref": cognitoUserPoolClientRef
                        },
                        "ProviderName": {
                            "Fn::GetAtt": [
                                cognitoUserPoolRef,
                                "ProviderName"
                            ]
                        }
                    }
                ]
            }
        },
    }
}
module.exports = {
    buildIdentityPool,
    buildCognitoIdentityPoolRoleAttachment
}