import {postRequest} from "./get-request";


export const Intercom = {
    /**
     * Send custom attributes to intercom
     * @param receiver
     * @param verificationCode
     * @param intercomAccessToken
     * @returns {Promise<unknown>}
     */
    async createIntercomUser(receiver, verificationCode, intercomAccessToken) {
        const headers = {
            'Authorization': `Bearer ${intercomAccessToken}`,
            'Accept': 'application/json'
        }
            const createUserBody = {
                "role": "user",
                "external_id": receiver['sub'],
                "email": receiver['email'] || "",
                "phone": receiver['phone_number'] || "",
                "custom_attributes": {
                    'activation_code': verificationCode,
                    'user_type': receiver['custom:user_group']
                }
            }
            await postRequest(
                'api.intercom.io',
                `/contacts/`,
                createUserBody,
                headers
            )
        // }
    }
}
