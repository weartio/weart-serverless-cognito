import {handler, SMS} from '../src/functions/verification_message/sms';
import {Decryption} from '../src/functions/verification_message/decryption';
import {Slack} from '../src/functions/verification_message/slack';


describe('Send Custom SMS', () => {
    beforeAll(() => {
        jest.resetModules() // Most important - it clears the cache
        jest.spyOn(Decryption, 'decode').mockImplementation(async () => 'code');
        jest.spyOn(SMS, 'send').mockImplementation(async () => 'MESSAGE-ID');
        jest.spyOn(Slack, 'notify').mockImplementation(async () => null);
    });


    it('Should send sms', async () => {
        const event = {
            triggerSource: 'CustomMessage_SignUp',
            request: {
                userAttributes: {
                    phone_number: "+4915211796459"
                },
                code: "123"
            }
        }

        const result = await handler(event);
        expect(result).toBe(event);
    })
})