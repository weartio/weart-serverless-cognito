/**
 * 
 * @param {*} refName 
 * @returns 
 */
function buildLambdaTriggerRole(refName = "LambdaTriggerRole") {
    return {
        [refName]: {
            "Type": "AWS::IAM::Role",
            "Properties": {
                "AssumeRolePolicyDocument": {
                    "Version": "2012-10-17",
                    "Statement": [
                        {
                            "Effect": "Allow",
                            "Action": "sts:AssumeRole",
                            "Principal": {
                                "Service": "lambda.amazonaws.com"
                            }
                        }
                    ]
                },
                "ManagedPolicyArns": [
                    "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
                ]
            }
        },
    }
}

/**
 * 
 * @param {*} refName 
 * @returns 
 */
function buildCognitoFunctionRole(rcsPrefix, refName = "CognitoFunctionsRole") {
    // @TODO: review the policies access
    return {
        [refName]: {
            "Type": "AWS::IAM::Role",
            "Properties": {
                "RoleName": `${rcsPrefix}-CognitoFunctionsRole`,
                "AssumeRolePolicyDocument": {
                    "Version": "2012-10-17",
                    "Statement": [
                        {
                            "Effect": "Allow",
                            "Principal": {
                                "Service": [
                                    "lambda.amazonaws.com"
                                ]
                            },
                            "Action": "sts:AssumeRole"
                        }
                    ]
                },
                "Policies": [
                    {
                        "PolicyName": `${rcsPrefix}-myPolicyName`,
                        "PolicyDocument": {
                            "Version": "2012-10-17",
                            "Statement": [
                                {
                                    "Effect": "Allow",
                                    "Action": [
                                        "*"
                                    ],
                                    "Resource": "*"
                                }
                            ]
                        }
                    }
                ]
            }
        },
    }
}

module.exports = {
    buildCognitoFunctionRole,
    buildLambdaTriggerRole
}