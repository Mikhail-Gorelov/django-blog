describe("Authorised behaviour spec", () => {
  it("authorise", () => {
    cy.intercept('POST', '/auth/sign-in').as('formSubmission')
    cy.getCookies().then((cookies) => {
      expect(cookies).to.have.length(0)
    })
    cy.visit("/")
    cy.get('#signInButton').click()
    cy.get('#email').type('root@root.ru')
    cy.get('#password').type('root')
    cy.get('#signInButtonLogin').click()
    cy.wait('@formSubmission')
    cy.url().should('include', '/')
    cy.getCookies().then((cookies) => {
      expect(cookies).to.have.length.above(0)
      cy.get('#home').click()
      cy.get('#posts').click()
      cy.get('#contact').click()
      cy.get('#about').click()
      cy.get('#profile').click()
      cy.url().should('include', '/user-profile')
      cy.go(-1)
      cy.get('#logOff').click()
    })
    cy.getCookies().then((cookies) => {
      expect(cookies).to.have.length(1)
    })
  });
});
