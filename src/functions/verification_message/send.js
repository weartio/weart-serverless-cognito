import {Decryption} from "./decryption";
import {Slack} from "./slack";
import {Intercom} from "./intercom";


/**
 *
 * @param event
 * @param receiverFunction
 * @param sendFunction
 * @returns {Promise<void>}
 */
export const execute = async (event, receiverFunction, sendFunction) => {
    /**
     ((event.triggerSource))
        'CustomMessage_SignUp':
        'CustomMessage_AdminCreateUser':
        'CustomMessage_ResendCode':
        'CustomMessage_ForgotPassword':
        'CustomMessage_UpdateUserAttribute':
        'CustomMessage_VerifyUserAttribute':
        'CustomMessage_Authentication':
     */

    const {request} = event;
    const code = request.code;
    const receiver = receiverFunction(request);
    const {email, phone_number} = receiver;
    const verificationCode = await Decryption.getDecryptedCode(code);
    const stage = process.env.STAGE;

    try {
        const message = `User ${email || phone_number}, verification code: ${verificationCode}`
        console.log(message)
        await Slack.notify(message)
        console.log("Ok")
    } catch (error) {
        console.log("Can't send message to slack", error)
    }

    try {
        const intercomAccessToken = process.env.INTERCOM_ACCESS_TOKEN;
        if (intercomAccessToken) {
            await Intercom.createIntercomUser(receiver, verificationCode, intercomAccessToken)
            console.log("Ok")
        }
    } catch (error) {
        console.log("Can't send message to intercom", error)
    }

    // if not prod don't send message, it will be visible at slack
    if (!(stage in ['dev', 'qa'])) {
        //@TODO: this might cause error by the provider, we need to solve it at the error center.
        await sendFunction(receiver, verificationCode);
    }
}