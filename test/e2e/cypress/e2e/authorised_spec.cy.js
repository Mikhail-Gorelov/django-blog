describe("Authorised behaviour spec", () => {
  it("authorise", () => {
    cy.intercept('POST', '/auth/sign-in').as('formSubmission')
    cy.getCookies().then((cookies) => {
      expect(cookies).to.have.length(0)
    })
    cy.visit("/")
    cy.get('#signInButton').should('be.visible').click()
    cy.get('#email').should('be.visible').type('root@root.ru')
    cy.get('#password').should('be.visible').type('root')
    cy.get('#signInButtonLogin').should('be.visible').click()
    cy.wait('@formSubmission')
    cy.url().should('include', '/')
    cy.getCookies().then((cookies) => {
      expect(cookies).to.have.length.above(0)
      cy.get('#home').should('be.visible').click()
      cy.get('#posts').should('be.visible').click()
      cy.get('#contact').should('be.visible').click()
      cy.get('#about').should('be.visible').click()
      cy.get('#profile').should('be.visible').click()
      cy.url().should('include', '/user-profile')
      cy.go(-1)
      cy.get('#logOff').should('be.visible').click()
    })
  });
});
