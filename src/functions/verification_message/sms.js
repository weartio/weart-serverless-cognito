import {execute} from "./send";

export const SMS = {
    async send(to, code) {
        const {TWILLIO_ACCOUNT_SID, TWILLIO_AUTH_TOKEN, TWILLIO_SENDING_NUMBER} = process.env;
        const client = require('twilio')(TWILLIO_ACCOUNT_SID, TWILLIO_AUTH_TOKEN);

        const message = await client.messages.create({
            to: to['phone_number'],
            from: TWILLIO_SENDING_NUMBER,
            body: `Verification code is: ${code}`,
        });

        return message.sid;
    },
    /**
     *
     * @param request
     * @returns {*}
     */
    getReceiver(request) {
        const {userAttributes} = request;
        return userAttributes;
    }
}

export const handler = async (event) => {
    await execute(event, SMS.getReceiver, SMS.send);
    return event;
}