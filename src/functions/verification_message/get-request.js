const https = require('https');

/**
 *
 * @param host
 * @param url
 * @param body
 * @returns {Promise<unknown>}
 */
export function postRequest(host, url, body) {
    const options = {
        hostname: host,
        path: url,
        method: 'POST',
        port: 443, // 👈️ replace with 80 for HTTP requests
        headers: {
            'Content-Type': 'application/json',
        },
    };

    return new Promise((resolve, reject) => {
        const req = https.request(options, res => {
            let rawData = '';

            res.on('data', chunk => {
                rawData += chunk;
            });

            res.on('end', () => {
                try {
                    resolve(rawData);
                } catch (err) {
                    reject(new Error(err));
                }
            });
        });

        req.on('error', err => {
            reject(new Error(err));
        });

        // 👇️ write the body to the Request object
        req.write(JSON.stringify(body));
        req.end();
    });
}
