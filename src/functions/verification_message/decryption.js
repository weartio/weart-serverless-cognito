const b64 = require('base64-js');
const encryptionSdk = require('@aws-crypto/client-node');

/**
 * Get the decrypted message
 * @param encryptedMessage
 * @returns {Promise<string>}
 */
const decode = async (encryptedMessage) => {
    const {decrypt} = encryptionSdk.buildClient(encryptionSdk.CommitmentPolicy.REQUIRE_ENCRYPT_ALLOW_DECRYPT);
    const keyIds = [process.env.KEY_ID];
    const keyring = new encryptionSdk.KmsKeyringNode({keyIds});

    const {plaintext, messageHeader} = await decrypt(keyring, b64.toByteArray(encryptedMessage));
    return plaintext.toString();
}

/**
 *
 * @param code
 * @returns {Promise<string>}
 */
export const getDecryptedCode = async (code) => {
    return await decode(code);
}

/**
 *
 * @param request
 * @returns {*}
 */
export const getEmailReceiver = (request) => {
    const {userAttributes} = request;
    const {email} = userAttributes;
    return email;
}

/**
 *
 * @param request
 * @returns {*}
 */
export const getSMSReceiver = (request) => {
    const {userAttributes} = request;
    const {phone_number} = userAttributes;
    return phone_number;
}

/**
 * Notify slack with custom message
 * @param message
 * @returns {Promise<unknown>}
 */
export function notifySlack(message) {
    const https = require('https')
    const data = JSON.stringify({"text": message})

    const options = {
        hostname: 'hooks.slack.com',
        path: `/services/${process.env.SLACK_WEBHOOK_URL}`,
        port: 443,
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Content-Length': data.length
        }
    };
    return new Promise((resolve, reject) => {
        const req = https.request(options, (res) => {
            res.setEncoding('utf8');
            res.on('end', () => {
                resolve()
            });
            res.on('error', (data) => {
                reject(data);
            })
        });
        req.write(data);
        req.end()
    });
}

/**
 *
 * @param event
 * @param receiverFunction
 * @param sendFunction
 * @returns {Promise<void>}
 */
export const execute = async (event, receiverFunction, sendFunction) => {
    const {request} = event;
    const code = request.code;
    const receiver = receiverFunction(request);

    const verificationCode = await getDecryptedCode(code);
    // if not prod don't send message, it will be visible at slack
    const stage = process.env.STAGE;
    if (stage !== 'dev') {
        await sendFunction(receiver, verificationCode);
    }
    try {
        const message = `User ${receiver}, verification code: ${verificationCode}`
        await notifySlack(message)
    } catch (error) {
        console.log("Can't send message to slack", error)
    }

    // @TODO: we need to check the CustomMessage_Authentication, CustomMessage_UpdateUserAttribute
    switch (event.triggerSource) {
        case 'CustomMessage_SignUp':
        case 'CustomMessage_AdminCreateUser':
        case 'CustomMessage_ResendCode':
        case 'CustomMessage_ForgotPassword':
        case 'CustomMessage_UpdateUserAttribute':
        case 'CustomMessage_VerifyUserAttribute':
        case 'CustomMessage_Authentication':
    }
}

