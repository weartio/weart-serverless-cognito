'use strict';

const { buildAppleIdentityProvider } = require("./resources/apple");
const { buildGoogleIdentityProvider } = require("./resources/google");
const { buildIdentityPool, buildCognitoIdentityPoolRoleAttachment } = require("./resources/IdentityPool");
const { buildKmsKey, buildLambdaTriggerRoleKmsPolicy } = require("./resources/kms");
const { buildLambdaTriggerInvokePermissionSMSSender, buildLambdaTriggerInvokePermissionEmailSender } = require("./resources/permissions");
const { buildLambdaTriggerRole, buildCognitoFunctionRole } = require("./resources/roles");
const { buildSnsTopic } = require("./resources/sns");
const { buildCongitoSMSRole, buildCognitoUserPool, buildCognitoAuthRole, buildCognitoUnAuthRole } = require("./resources/userPool");
const { buildUserPoolClient } = require("./resources/userPoolClient");
const { buildUserPoolDomain } = require("./resources/userPoolDomain");

const Resource = require("./resources/resource");

/**
 * 
 */
class WeArtCongitoPlugin {

  constructor(serverless, options) {
    this.serverless = serverless;
    this.provider = this.serverless.getProvider('aws');
    const service = this.serverless.service;

    this.options = service.custom;

    if (!this.options) {
      throw new Error("Custom field is missing");
    }
    if (!service.custom.cognito) {
      throw new Error("Cognito field from custom is missing");
    }
    this.options = service.custom.cognito;

    this.stackName = this.serverless.service.service;
    this.stage = service.provider ? service.provider.stage : service.stage;
    this.rcsPrefix = `${this.stackName}-${this.stage}`
    this.domain = `auth-${this.stage}.manzilik.com`
    this.smsExternalId = this.options.smsExternalId
    this.loginCallbackUrl = this.options.loginCallbackUrl
    this.logoutCallbackUrl = this.options.logoutCallbackUrl
    this.deleletionPolicy = this.options.deleletionPolicy

    this.hooks = {
      'after:package:initialize': this.afterInitialize.bind(this),
    };
  }

  log(message, options) {
    this.serverless.cli.log(message, 'WeArt Cognito Plugin', options);
  }

  /**
   * 
   * @param {Resource} newResource 
   */
  appendResrouce(newResource) {
    const providerObj = this.serverless.service.provider;
    const resources = providerObj.compiledCloudFormationTemplate.Resources;
    Object.assign(
      resources,
      newResource.json,
    )
  }

  afterInitialize() {
    this.serverless.cli.log('Start generateing the resources');

    const customSMSSenderArn = this.options.customSMSSenderArn;
    const customEmailSenderArn = this.options.customEmailSenderArn;

    /**
     * KSM
     * 1- SMS Role
     * 2- KmsKey
     * 3- LambdaTriggerRole
     * 4- LambdaTriggerRolePolicy on Ksm resource
     */

    let smsRole = {};
    
    smsRole = new Resource(buildCongitoSMSRole(this.rcsPrefix, this.smsExternalId));
    this.appendResrouce(smsRole);
  

    const kmsResource = new Resource(buildKmsKey());
    const lambdaTriggerRole = new Resource(buildLambdaTriggerRole())
    const lambdaTriggerRolePolicy = new Resource(buildLambdaTriggerRoleKmsPolicy(kmsResource.ref, lambdaTriggerRole.ref));
    this.appendResrouce(kmsResource);
    this.appendResrouce(lambdaTriggerRole);
    this.appendResrouce(lambdaTriggerRolePolicy);
    /**
     * UserPool
     * 1- Userpool
     * 2- Google  --> if google config are provided
     * 3- Apple   --> if apple config are provided
     * 4- UserPoolDomain
     * 5- UserpoolClient
     */

    const userPool = new Resource(buildCognitoUserPool(this.rcsPrefix, kmsResource.ref, smsRole.ref, customEmailSenderArn, customSMSSenderArn, this.smsExternalId));

    if (customSMSSenderArn) {
      const lambdaTriggerInvokePermissionSMSSender = new Resource(buildLambdaTriggerInvokePermissionSMSSender(customSMSSenderArn, userPool.ref));
      this.appendResrouce(lambdaTriggerInvokePermissionSMSSender);
    }

    if (customEmailSenderArn) {
      const lambdaTriggerInvokePermissionEmailSender = new Resource(buildLambdaTriggerInvokePermissionEmailSender(customEmailSenderArn, userPool.ref));
      this.appendResrouce(lambdaTriggerInvokePermissionEmailSender);
    }
    let google = {};
    let apple = {};

    if (this.options.hasOwnProperty("google") &&
      this.options.google.hasOwnProperty("clientId") &&
      this.options.google.hasOwnProperty("clientSecret")) {
      const googleClientId = this.options.google.clientId;
      const googleClientSecret = this.options.google.clientSecret;
      google = new Resource(buildGoogleIdentityProvider(googleClientId, googleClientSecret, userPool.ref));
      this.appendResrouce(google);
    }


    if (this.options.hasOwnProperty('apple') &&
      this.options.apple.hasOwnProperty('clientId') &&
      this.options.apple.hasOwnProperty('teamId') &&
      this.options.apple.hasOwnProperty('keyId') &&
      this.options.apple.hasOwnProperty('privateKey')
    ) {
      const appleClientId = this.options.apple.clientId;
      const appleTeamId = this.options.apple.teamId;
      const appleKeyId = this.options.apple.keyId;
      const applePrivateKey = this.options.apple.privateKey;

      apple = new Resource(buildAppleIdentityProvider(appleClientId, appleTeamId, appleKeyId, applePrivateKey, userPool.ref));
      this.appendResrouce(apple);
    }
    const userPoolDomain = new Resource(buildUserPoolDomain(this.domain, userPool.ref));

    const userPoolClient = new Resource(buildUserPoolClient(this.rcsPrefix, google, apple, userPool.ref, this.loginCallbackUrl, this.logoutCallbackUrl));

    this.appendResrouce(userPool)
    this.appendResrouce(userPoolDomain);
    this.appendResrouce(userPoolClient);


    const identityPool = new Resource(buildIdentityPool(this.rcsPrefix, userPool.ref, userPoolClient.ref, this.deleletionPolicy));
    const authRole = new Resource(buildCognitoAuthRole(this.rcsPrefix, identityPool.ref));
    const unAuthRole = new Resource(buildCognitoUnAuthRole(this.rcsPrefix, identityPool.ref));

    const identityPoolRoleAttachments = new Resource(buildCognitoIdentityPoolRoleAttachment(identityPool.ref,
      authRole.ref, unAuthRole.ref));

    this.appendResrouce(identityPool);
    this.appendResrouce(authRole);
    this.appendResrouce(unAuthRole);
    this.appendResrouce(identityPoolRoleAttachments);

    // Roles & Permissions
    const cognitoFunctionRole = new Resource(buildCognitoFunctionRole(this.rcsPrefix))
    this.appendResrouce(cognitoFunctionRole)

    // SNS Topic
    const snsTopic = new Resource(buildSnsTopic(this.rcsPrefix))
    this.appendResrouce(snsTopic);
  }

}

module.exports = WeArtCongitoPlugin;