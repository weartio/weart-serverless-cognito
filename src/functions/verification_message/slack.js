import {postRequest} from "./get-request";

export const Slack = {
    /**
     * Notify slack with custom message
     * @param message
     * @returns {Promise<unknown>}
     */
    async notify(message) {
        const body = {"text": message}
        await postRequest('hooks.slack.com', `/services/${process.env.SLACK_WEBHOOK_URL}`, body)
    }
}
