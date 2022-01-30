const { kms } = require("../src/resources/kms");
const Resource = require("../src/resources/resource");
const { cognitoUserPool, congitoSMSRole } = require("../src/resources/userPool");

describe('Create UserPool Resource', () => {
    it('should create the full resource', () => {
        const kmsRES = new Resource("Kms", kms, "KmsKey")
        const smsRole = new Resource("congitoSMSRole", congitoSMSRole)   
        const resource = new Resource("CognitoUserPool", cognitoUserPool, kmsRES.ref, smsRole.ref, true, true)

        console.log(JSON.stringify(resource));
    })
});