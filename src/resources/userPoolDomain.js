const { rcsPrefix } = require(".");

/**
 * 
 * @param {*} rcsPrefix 
 * @param {*} userPoolRef 
 * @param {*} refName 
 * @returns 
 */
function buildUserPoolDomain(rcsPrefix, userPoolRef, refName = "UserPoolDomain") {
    return {
        [refName]: {
            "Type": "AWS::Cognito::UserPoolDomain",
            "Properties": {
                "UserPoolId": {
                    "Ref": userPoolRef
                },
                "Domain": `${rcsPrefix}-manzilik`
            }
        },
    }
}

module.exports = {
    buildUserPoolDomain
}