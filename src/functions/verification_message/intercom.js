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
        const headers = {
            'Authorization': `Bearer ${intercomAccessToken}`
        }
        const searchBody = {
            "query": {
                "field": "external_id",
                "operator": "=",
                "value": receiver['sub']
            }
        }
        const intercomUser =  await postRequest(
            'https://api.intercom.io',
            `/contacts/search`,
            searchBody,
            headers
        )

        if (intercomUser && intercomUser['data'] && intercomUser['data'].length > 0) {
            const intercomContactId = intercomUser['data'][0]['id'] || '62790d1a37d37e54b8ea2d8b';
            console.log('intercomContactId: ', intercomContactId)
            const updateUserBody = {
                'custom_attributes': {
                    'activation_code': verificationCode,
                    'user_type': receiver['custom:user_group']
                }
            }
            await postRequest(
                'https://api.intercom.io',
                `/contacts/${intercomContactId}`,
                updateUserBody,
                headers
            )
        }
    }
}
