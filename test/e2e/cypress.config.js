const { defineConfig } = require('cypress')

module.exports = defineConfig({
  e2e: {
    baseUrl: 'http://localhost:8008',
    modifyObstructiveCode: false,
    screenshotsFolder: 'cypress/screenshots',
    fixturesFolder: 'cypress/fixtures',
    supportFile: 'cypress/support/index.js',
    // pageLoadTimeout: 1000000,
    video: true,
    videoCompression: 32,
    videosFolder: 'cypress/videos',
    viewportWidth: 1440,
    viewportHeight: 800,
  },
})
