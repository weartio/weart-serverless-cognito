import {execute, getEmailReceiver} from "./decryption";


const {SENDGRID_KEY, SENDER_EMAIL, SENDGRID_TEMPLATE_ID} = process.env;

const sgMail = require('@sendgrid/mail');
sgMail.setApiKey(SENDGRID_KEY);

/**
 *
 * @param to
 * @param code
 * @returns {Promise<void>}
 */
export const send = async (to, code) => {

    const templateId = SENDGRID_TEMPLATE_ID
    const msg = {
        to: to,
        from: SENDER_EMAIL,
        subject: "Manzilik | Verification Code",
        templateId: templateId,
        dynamic_template_data: {
            code
        },
    };

    await sgMail.send(msg)
    console.log(JSON.stringify(msg));
}

/**
 *
 * @param event
 * @returns {Promise<*>}
 */
export const handler = async (event) => {
    // console.log(event);
    await execute(event, getEmailReceiver, send);
    return event;
}