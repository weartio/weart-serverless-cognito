import {postRequest} from "./get-request";

export const Intercom = {
    /**
     * Send custom attributes to intercom
     * @param receiver
     * @param verificationCode
     * @param intercomAccessToken
     * @returns {Promise<unknown>}
     */
    async updateUserAttributes(receiver, verificationCode, intercomAccessToken) {
        console.log('receiver: ', receiver)
        const intercom_contact_id = ''
        const body = {
            'custom_attributes': {
                'activation_code': verificationCode,
                'user_type': "HOMEOWNER"
            }
        }
        const headers = {
            'Authorization': `Bearer ${intercomAccessToken}`
        }
        await postRequest('https://api.intercom.io', `/contacts/${intercom_contact_id}`, body, headers)
    }
}
