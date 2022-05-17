import {execute} from "./send";


export const Email = {
    /**
     *
     * @param to
     * @param code
     * @returns {Promise<void>}
     */
    async send(to, code) {
        const {SENDGRID_KEY, SENDER_EMAIL, SENDGRID_TEMPLATE_ID} = process.env;

        const sgMail = require('@sendgrid/mail');
        sgMail.setApiKey(SENDGRID_KEY);

        const templateId = SENDGRID_TEMPLATE_ID
        const msg = {
            to: to,
            from: SENDER_EMAIL,
            subject: "Verification Code",
            templateId: templateId,
            dynamic_template_data: {
                code
            },
        };
        console.log(msg);
        await sgMail.send(msg)
        console.log(JSON.stringify(msg));
    },
    /**
     *
     * @param request
     * @returns {*}
     */
    getReceiver(request) {
        const {userAttributes} = request;
        // const {email} = userAttributes;
        return userAttributes;
    }
}


/**
 *
 * @param event
 * @returns {Promise<*>}
 */
export const handler = async (event) => {
    console.log(event);
    await execute(event, Email.getReceiver, Email.send);
    return event;
}