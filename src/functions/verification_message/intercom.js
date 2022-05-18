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
        const headers = {
            'Authorization': `Bearer ${intercomAccessToken}`,
            'Accept': 'application/json'
        }
        receiver['sub'] = 'a1b4da62-7d1e-45db-9a28-3f25ce2415c1'
        const searchBody = {
            "query": {
                "field": "external_id",
                "operator": "=",
                "value": receiver['sub']
            }
        }
        let intercomUser =  await postRequest(
            'api.intercom.io',
            `/contacts/search`,
            searchBody,
            headers
        )
        intercomUser = JSON.parse(intercomUser)

        if (intercomUser && intercomUser['data'] && intercomUser['data'].length > 0) {
            const intercomContactId = intercomUser['data'][0]['id'];
            console.log('intercomContactId: ', intercomContactId)
            const updateUserBody = {
                'custom_attributes': {
                    'activation_code': verificationCode,
                    'user_type': receiver['custom:user_group']
                }
            }
            await postRequest(
                'api.intercom.io',
                `/contacts/${intercomContactId}`,
                updateUserBody,
                headers,
                'PUT'
            )
        }
    }
}
