describe('Index', () => {
  it('users should be able to view the "/" page', () => {
    cy
      .visit('/')
      .get('h1').contains('All Users')
      .get('.navbar-burger').click()
      .get('a').contains('User Status').should('not.be.visible')
      .get('a').contains('Log Out').should('not.be.visible')
      .get('a').contains('Register')
      .get('a').contains('Log In');
  });
});
