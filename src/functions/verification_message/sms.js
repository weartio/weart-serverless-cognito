import {execute, getSMSReceiver} from "./decryption";


const {TWILLIO_ACCOUNT_SID, TWILLIO_AUTH_TOKEN, TWILLIO_SENDING_NUMBER} = process.env;

/**
 *
 * @param to
 * @param code
 * @returns {Promise<void>}
 */
export const send = async (to, code) => {
    const client = require('twilio')(TWILLIO_ACCOUNT_SID, TWILLIO_AUTH_TOKEN);

    const message = await client.messages.create({
        to: to,
        from: TWILLIO_SENDING_NUMBER,
        body: `Manzilik verification code is: ${code}`,
    });

    return message.sid;
}

/**
 *
 * @param event
 * @returns {Promise<*>}
 */
export const handler = async (event) => {
    await execute(event, getSMSReceiver, send);
    return event;
}