const { userPoolDomain } = require("../src/resources/userPoolDomain");

describe('Create UserPoolDomain Resource', () => {
    it('should create the full resource', () => {
        const resource = userPoolDomain("CognitoUserPool");
        console.log(JSON.stringify(resource));
    })
});