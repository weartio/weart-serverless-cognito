import {Email, handler} from '../src/functions/verification_message/email';
import {Decryption} from '../src/functions/verification_message/decryption';
import {Slack} from '../src/functions/verification_message/slack';


describe('Send Custom Email', () => {
    beforeAll(() => {
        jest.resetModules() // Most important - it clears the cache
        jest.spyOn(Decryption, 'decode').mockImplementation(async () => 'code');
        jest.spyOn(Email, 'send').mockImplementation(async () => 'MESSAGE-ID');
        jest.spyOn(Slack, 'notify').mockImplementation(async () => null);
    });


    it('Should send email', async () => {
        const event = {
            triggerSource: 'CustomMessage_SignUp',
            request: {
                userAttributes: {
                    email: "mostafa.balata@gmail.com"
                },
                code: "123"
            }
        }

        const result = await handler(event);
        expect(result).toBe(event);
    })
})