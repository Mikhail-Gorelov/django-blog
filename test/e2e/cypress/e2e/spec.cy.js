describe("Default behaviour spec", () => {
  it("check default behaviour", () => {
    cy.visit("/")
    cy.get('#home').click()
    cy.get('#posts').click()
    cy.get('#contact').click()
    cy.get('#about').click()
  });
});
