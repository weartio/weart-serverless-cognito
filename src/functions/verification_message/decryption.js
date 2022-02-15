const b64 = require('base64-js');
const encryptionSdk = require('@aws-crypto/client-node');

export const Decryption = {
    /**
     * Get the decrypted message
     * @param encryptedMessage
     * @returns {Promise<string>}
     */
    async decode(encryptedMessage) {
        const {decrypt} = encryptionSdk.buildClient(encryptionSdk.CommitmentPolicy.REQUIRE_ENCRYPT_ALLOW_DECRYPT);
        const keyIds = [process.env.KEY_ID];
        const keyring = new encryptionSdk.KmsKeyringNode({keyIds});

        const {plaintext, messageHeader} = await decrypt(keyring, b64.toByteArray(encryptedMessage));
        return plaintext.toString();
    },

    /**
     *
     * @param code
     * @returns {Promise<string>}
     */
    async getDecryptedCode(code) {
        const decodedMessage = await Decryption.decode(code);
        return decodedMessage
    }
}
