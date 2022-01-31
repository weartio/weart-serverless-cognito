# weart-serverless-cognito

Amazon Cognito lets you add user sign-up, sign-in, and access control to your web and mobile apps quickly and easily. Amazon Cognito scales to millions of users and supports sign-in with social identity providers, such as Apple, Facebook, Google, and Amazon, and enterprise identity providers via SAML 2.0 and OpenID Connect

This plugin is making the process of adding cognito to your project peace of cake.



## Installation

Use the package manager [npm](https://www.npmjs.com/) to install the plugin.

```bash
npm install git://github.com/weartio/weart-serverless-cognito.git
```


# How it works
![image description](user_pool.drawio.svg)

todo



# Testing
todo





## Usage

```yaml

service: projectname
frameworkVersion: "3"
useDotenv: true

provider:
  name: aws
  region: eu-central-1
  stage: ${opt:stage,'dev'}

plugins:
  - serverless-bundle # this to help bundling the lambda functions
  - weart-serverless-cognito # this is our lovely plugin

package:
  individually: true
  exclude:
    - "**/*"

# if you want to have the full benifits from our workflow use our labmda functions, otherwise feel free to write your own ones.
functions:
  - ${file(node_modules/weart-serverless-cognito/serverless.yml):functions}


custom:
  currentStage: ${self:service}-${opt:stage, self:provider.stage}
  cognito:
    functionsPath: "node_modules/weart-cognito/src/functions"
    customSMSSenderArn: "arn:aws:lambda:eu-central-1:${aws:accountId}:function:${self:custom.currentStage}-customSMSSender"
    customEmailSenderArn: "arn:aws:lambda:eu-central-1:${aws:accountId}:function:${self:custom.currentStage}-customEmailSender"
    smsExternalId: "1f1d7538-6e07-46e6-b0c4-5a2a0bd16215"
    loginCallbackUrl: ${env:LOGIN_CALLBACK_URL}
    logoutCallbackUrl: ${env:LOGOUT_CALLBACK_URL}
    deleletionPolicy: Delete
    platformAllowedScope: "phone_number,email,google"
    keys:
      SENDGRID_KEY: ${env:SENDGRID_KEY}
      SENDGRID_TEMPLATE_ID: ${env:SENDGRID_TEMPLATE_ID}
      SENDER_EMAIL: ${env:SENDER_EMAIL}
      TWILLIO_ACCOUNT_SID: ${env:TWILLIO_ACCOUNT_SID}
      TWILLIO_AUTH_TOKEN: ${env:TWILLIO_AUTH_TOKEN}
      TWILLIO_SENDING_NUMBER: ${env:TWILLIO_SENDING_NUMBER}
      SLACK_WEBHOOK_URL: ${env:SLACK_WEBHOOK_URL}
    google:
      clientId: ${env:GOOGLE_CLIENT_ID}
      clientSecret: ${env:GOOGLE_CLIENT_SECRET}
    apple:
      clientId: ${env:APPLE_CLIENT_ID}
      teamId: ${env:APPLE_TEAM_ID}
      keyId: ${env:APPLE_KEY_ID}
      privateKey: ${env:APPLE_PRIVATE_KEY}
```




## License
[MIT](https://choosealicense.com/licenses/mit/)