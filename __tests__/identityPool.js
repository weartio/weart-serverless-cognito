const { identityPool, cognitoIdentityPoolRoleAttachment } = require("../src/resources/IdentityPool");

describe('Create KMS Resource', () => {

    it('should create the full resource', () => {
        const resource = identityPool();
        console.log(JSON.stringify(resource));
    })

    it('should create the full resource', () => {
        const resource = cognitoIdentityPoolRoleAttachment("CognitoIdentityPool", "CognitoAuthRole", "CognitoUnAuthRole", "CognitoIdentityPoolRoleAttachment");
        console.log(JSON.stringify(resource));
    })
})