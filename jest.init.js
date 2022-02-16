const dotenv = require('dotenv')
jest.setTimeout(10000)
dotenv.config({
    path: './.env.test'
});