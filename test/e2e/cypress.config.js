const {defineConfig} = require("cypress");

module.exports = defineConfig({
  // http://localhost:8008 - for local use
  e2e: {
    baseUrl: "http://localhost:8008",
    pageLoadTimeout: 10000,
    defaultCommandTimeout: 8000,
    modifyObstructiveCode: false,
    screenshotsFolder: "cypress/screenshots",
    fixturesFolder: "cypress/fixtures",
    supportFile: "cypress/support/index.js",
    video: true,
    videoCompression: 32,
    videosFolder: "cypress/videos",
    viewportWidth: 1440,
    viewportHeight: 800,
  },
});
