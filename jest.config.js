module.exports = {
    moduleFileExtensions: ["js", "json", "json"],
    transform: {
        '^.+\\.(js)?$': 'babel-jest'
    },
    testEnvironment: 'node',
    moduleNameMapper: {
        '^@/(.*)$': '<rootDir>/$1'
    },
    testMatch: [
        '<rootDir>/__tests__/*.(js|jsx)'
    ],
    setupFiles: ['<rootDir>/jest.init.js'],
    transformIgnorePatterns: ['<rootDir>/node_modules/']
};