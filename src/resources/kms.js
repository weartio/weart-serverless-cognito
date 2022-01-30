const { getResourceArn } = require("./uilts")

function generateKeyPolicy() {
    // @TODO: review the principal and the resources.
    return {
        "KeyPolicy": {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {
                        "AWS": {
                            "Fn::Sub": "arn:aws:iam::${AWS::AccountId}:root"
                        }
                    },
                    "Action": "kms:*",
                    "Resource": "*"
                }
            ]
        }
    }
}


/**
 * 
 * @param {*} kmsKeyRef 
 * @param {*} lambdaTriggerRoleRef 
 * @param {*} refName 
 * @returns 
 */
function buildLambdaTriggerRoleKmsPolicy(kmsKeyRef, lambdaTriggerRoleRef, refName = "LambdaTriggerRoleKmsPolicy") {
    return {
        [refName]: {
            "Type": "AWS::IAM::Policy",
            "Properties": {
                "PolicyDocument": {
                    "Version": "2012-10-17",
                    "Statement": [
                        {
                            "Effect": "Allow",
                            "Action": [
                                "kms:Decrypt"
                            ],
                            ...getResourceArn("Resource", kmsKeyRef)
                        }
                    ]
                },
                "PolicyName": "LambdaKmsPolicy",
                "Roles": [
                    {
                        "Ref": lambdaTriggerRoleRef
                    }
                ]
            }
        },
    }
}

/**
 * 
 * @param {*} client_id 
 * @param {*} team_id 
 * @param {*} key_id 
 * @param {*} private_key 
 * @param {*} cognitoUserPoolRef 
 * @returns 
 */
function buildKmsKey(refName = "KmsKey") {
    return {
        [refName]: {
            Type: 'AWS::KMS::Key',
            Properties: {
                Enabled: true,
                ...generateKeyPolicy()
            }
        }
    }
}

module.exports = {
    buildKmsKey,
    buildLambdaTriggerRoleKmsPolicy,
    generateKeyPolicy
}