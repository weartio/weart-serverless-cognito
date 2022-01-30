const { getResourceArn } = require('./uilts');
/**
 * 
 * @returns 
 */
function generateCogntioAuthRolePolicies(rcsPrefix) {
    return {
        "Policies": [
            {
                "PolicyName": `${rcsPrefix}-CognitoAuthorizedPolicy`,
                "PolicyDocument": {
                    "Version": "2012-10-17",
                    "Statement": [
                        {
                            "Effect": "Allow",
                            "Action": [
                                "mobileanalytics:PutEvents",
                                "cognito-sync:*",
                                "cognito-identity:*"
                            ],
                            "Resource": "*"
                        },
                        {
                            "Effect": "Allow",
                            "Action": [
                                "execute-api:Invoke"
                            ],
                            "Resource": "*"
                        }
                    ]
                }
            }
        ]
    }
}

/**
 * 
 * @param {*} cogntioUserPoolRef 
 * @param {*} isAuthenticated 
 * @returns 
 */
function generateAuthAssumeRolePolicyDocument(cogntioUserPoolRef, isAuthenticated) {
    return {
        "AssumeRolePolicyDocument": {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {
                        "Federated": "cognito-identity.amazonaws.com"
                    },
                    "Action": [
                        "sts:AssumeRoleWithWebIdentity"
                    ],
                    "Condition": {
                        "StringEquals": {
                            "cognito-identity.amazonaws.com:aud": {
                                "Ref": cogntioUserPoolRef
                            }
                        },
                        "ForAnyValue:StringLike": {
                            "cognito-identity.amazonaws.com:amr": isAuthenticated ? "authenticated" : "unauthenticated"
                        }
                    }
                }
            ]
        }
    }
}

/**
 * 
 * @param {*} cogntioUserPoolRef 
 * @returns 
 */
function buildCognitoAuthRole(rcsPrefix, cogntioUserPoolRef, refName = "CognitoAuthRole") {
    return {
        [refName]: {
            "Type": "AWS::IAM::Role",
            "DeletionPolicy": "Delete",
            "Properties": {
                "RoleName": `${rcsPrefix}-CognitoAuthRole`,
                "Path": "/",
                ...generateAuthAssumeRolePolicyDocument(cogntioUserPoolRef, true)
                , ...generateCogntioAuthRolePolicies(rcsPrefix)
            },
        }
    }
}

/**
 * 
 * @param {*} cogntioUserPoolRef 
 * @returns 
 */
function buildCognitoUnAuthRole(rcsPrefix, cogntioUserPoolRef, refName = "CognitoUnAuthRole") {
    return {
        [refName]: {
            "Type": "AWS::IAM::Role",
            "DeletionPolicy": "Delete",
            "Properties": {
                "RoleName": `${rcsPrefix}-CognitoUnAuthRole`,
                "Path": "/",
                ...generateAuthAssumeRolePolicyDocument(cogntioUserPoolRef, false)
                , ...generateCogntioAuthRolePolicies(rcsPrefix)
            },
        }
    }
}

/**
 * 
 * @returns 
 */
function buildCongitoSMSRole(rcsPrefix, smsExternalId, refName = "CognitoSMSRole") {
    return {
        [refName]: {
            "Type": "AWS::IAM::Role",
            "Properties": {
                "AssumeRolePolicyDocument": {
                    "Version": "2012-10-17",
                    "Statement": [
                        {
                            "Effect": "Allow",
                            "Principal": {
                                "Service": "cognito-idp.amazonaws.com"
                            },
                            "Action": [
                                "sts:AssumeRole"
                            ],
                            "Condition": {
                                "StringEquals": {
                                    "sts:ExternalId": smsExternalId
                                }
                            }
                        }
                    ]
                },
                "Policies": [
                    {
                        "PolicyDocument": {
                            "Version": "2012-10-17",
                            "Statement": [
                                {
                                    "Effect": "Allow",
                                    "Action": [
                                        "sns:Publish"
                                    ],
                                    "Resource": [
                                        "*"
                                    ]
                                }
                            ]
                        },
                        "PolicyName": `${rcsPrefix}-CognitoSendSMSPolicyName`
                    }
                ],
                "RoleName": `${rcsPrefix}-CognitoSMSRole`
            }
        }
    }
}


function customEmailSender(customEmailSenderArn) {

    return {
        "CustomEmailSender": {
            "LambdaArn": customEmailSenderArn,
            "LambdaVersion": "V1_0"
        },
    }
}

function customSMSSender(customSMSSenderArn) {
    return {
        "CustomSMSSender": {
            "LambdaArn": customSMSSenderArn,
            "LambdaVersion": "V1_0"
        },
    }
}

function buildCognitoUserPool(rcsPrefix, kmsKeyRef, cognitoSMSRoleRef, customEmailSenderArn, customSMSSenderArn, smsExternalId = null, refName = "CognitoUserPool") {
    return {
        [refName]: {
            "Type": "AWS::Cognito::UserPool",
            "DeletionPolicy": "Delete",
            "Properties": {
                "UserPoolName": `${rcsPrefix}-users`,
                "LambdaConfig": {
                    ...customEmailSenderArn ? customEmailSender(customEmailSenderArn) : {},
                    ...customSMSSenderArn ? customSMSSender(customSMSSenderArn) : {},
                    ...customEmailSenderArn || customSMSSenderArn ? getResourceArn("KMSKeyID", kmsKeyRef) : {}
                },
                "AutoVerifiedAttributes": [
                    "email",
                    "phone_number"
                ],
                "MfaConfiguration": "OPTIONAL",
                "SmsConfiguration": {
                    "ExternalId": smsExternalId,
                    ...getResourceArn("SnsCallerArn", cognitoSMSRoleRef),
                },
                "UsernameAttributes": [
                    "email",
                    "phone_number"
                ],
                "Schema": [
                    {
                        "Name": "access_token",
                        "AttributeDataType": "String",
                        "Mutable": true,
                        "Required": false
                    },
                    {
                        "Name": "platform",
                        "AttributeDataType": "String",
                        "Mutable": true,
                        "Required": false
                    },
                    {
                        "Name": "first_name",
                        "AttributeDataType": "String",
                        "Mutable": true,
                        "Required": false
                    },
                    {
                        "Name": "last_name",
                        "AttributeDataType": "String",
                        "Mutable": true,
                        "Required": false
                    },
                    {
                        "Name": "user_group",
                        "AttributeDataType": "String",
                        "Mutable": true,
                        "Required": false
                    },
                    {
                        "Name": "custom",
                        "AttributeDataType": "String",
                        "Mutable": true,
                        "Required": false
                    }
                ],
                "Policies": {
                    "PasswordPolicy": {
                        "RequireLowercase": true,
                        "RequireSymbols": false,
                        "RequireNumbers": true,
                        "MinimumLength": 8,
                        "RequireUppercase": false,
                        "TemporaryPasswordValidityDays": 7
                    }
                },
                "AdminCreateUserConfig": {
                    "AllowAdminCreateUserOnly": false
                }
            }
        },
    }
}


module.exports = {
    buildCognitoAuthRole,
    buildCognitoUnAuthRole,
    buildCongitoSMSRole,
    buildCognitoUserPool
}