describe("Default behaviour spec", () => {
  it("check default behaviour", () => {
    cy.visit("/")
    cy.get('#home').should('be.visible').click()
    cy.get('#posts').should('be.visible').click()
    cy.get('#contact').should('be.visible').click()
    cy.get('#about').should('be.visible').click()
  });
});
