describe("The Home Page", () => {
  it("successfully loads", () => {
    cy.visit("/");
  });
});

describe('template spec', () => {
  it('passes', () => {
    cy.visit('http://localhost:8008/'),
      cy.get('[data-testid="signUpButton"]').click()
  })
})
// click headers -> sign up -> login -> profile -> logout
// maybe test clicks on main navigation's points + videos

// cy.exec() - to run system commands
// cy.task() - to run code in Node via the setupNodeEvents function
// cy.request() - to make HTTP requests

// describe('The Login Page', () => {
//   beforeEach(() => {
//     // reset and seed the database prior to every test
//     cy.exec('npm run db:reset && npm run db:seed')
//
//     // seed a user in the DB that we can control from our tests
//     // assuming it generates a random password for us
//     cy.request('POST', '/test/seed/user', { username: 'jane.lane' })
//       .its('body')
//       .as('currentUser')
//   })
//
//   it('sets auth cookie when logging in via form submission', function () {
//     // destructuring assignment of the this.currentUser object
//     const { username, password } = this.currentUser
//
//     cy.visit('/login')
//
//     cy.get('input[name=username]').type(username)
//
//     // {enter} causes the form to submit
//     cy.get('input[name=password]').type(`${password}{enter}`)
//
//     // we should be redirected to /dashboard
//     cy.url().should('include', '/dashboard')
//
//     // our auth cookie should be present
//     cy.getCookie('your-session-cookie').should('exist')
//
//     // UI should reflect this user being logged in
//     cy.get('h1').should('contain', 'jane.lane')
//   })
// })

// In cypress/support/commands.js

// Cypress.Commands.add('login', (username, password) => {
//   cy.visit('/login')
//
//   cy.get('input[name=username]').type(username)
//
//   // {enter} causes the form to submit
//   cy.get('input[name=password]').type(`${password}{enter}`, { log: false })
//
//   // we should be redirected to /dashboard
//   cy.url().should('include', '/dashboard')
//
//   // our auth cookie should be present
//   cy.getCookie('your-session-cookie').should('exist')
//
//   // UI should reflect this user being logged in
//   cy.get('h1').should('contain', username)
// })
//
// // In your spec file
//
// it('does something on a secured page', function () {
//   const { username, password } = this.currentUser
//   cy.login(username, password)
//
//   // ...rest of test
// })

// do logout
// after(() => {
//   // runs once after all tests in the block
// })
