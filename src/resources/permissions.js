const { accountId, region } = require(".");
const { getResourceArn, capitalize } = require("./uilts");

/**
 * 
 * @param {*} refName 
 * @param {*} functionName 
 * @param {*} cognitoUserPoolRef 
 * @returns 
 */
function generatePermission(lambdaArn, refName, functionName, cognitoUserPoolRef) {
    return {
        [refName]: {
            "Type": "AWS::Lambda::Permission",
            "Properties": {
                "Action": "lambda:invokeFunction",
                "Principal": "cognito-idp.amazonaws.com",
                "FunctionName": lambdaArn,
                ...getResourceArn("SourceArn", cognitoUserPoolRef),
            },
            "DependsOn": [
                functionName
            ]
        }
    }
}

/**
 * 
 * @param {*} cognitoUserPoolRef 
 * @returns 
 */
function buildLambdaTriggerInvokePermissionEmailSender(lambdaArn, cognitoUserPoolRef) {
    return generatePermission(lambdaArn, "LambdaTriggerInvokePermissionEmailSender", "CustomEmailSenderLambdaFunction", cognitoUserPoolRef)
}

/**
 * 
 * @param {*} cognitoUserPoolRef 
 * @returns 
 */
function buildLambdaTriggerInvokePermissionSMSSender(lambdaArn, cognitoUserPoolRef) {
    return generatePermission(lambdaArn, "LambdaTriggerInvokePermissionSMSSender", "CustomSMSSenderLambdaFunction", cognitoUserPoolRef)
}

module.exports = {
    buildLambdaTriggerInvokePermissionEmailSender,
    buildLambdaTriggerInvokePermissionSMSSender
}