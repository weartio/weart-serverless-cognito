const https = require('https');

/**
 *
 * @param host
 * @param url
 * @param body
 * @param headers
 * @param httpMethod
 * @returns {Promise<unknown>}
 */
export function postRequest(host, url, body, headers={}, httpMethod='POST') {
    const options = {
        hostname: host,
        path: url,
        method: httpMethod,
        port: 443, // 👈️ replace with 80 for HTTP requests
        headers: {
            'Content-Type': 'application/json',
            ...headers
        },
    };

    return new Promise((resolve, reject) => {
        console.log('headers: ', options.headers)
        console.log('host: ', body)
        const req = https.request(options, res => {
            let rawData = '';

            res.on('data', chunk => {
                rawData += chunk;
            });

            res.on('end', () => {
                console.log('done: ', rawData)
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