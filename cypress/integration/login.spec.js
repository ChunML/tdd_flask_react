const randomstring = require('randomstring');

const username = randomstring.generate();
const email = `${username}@email.com`;
const password = 'ninechars';

describe('Log In', () => {
  it('should display the log in form', () => {
    cy
      .visit('/login')
      .get('h1').contains('Log In')
      .get('form')
      .get('input[disabled]')
      .get('.validation-list')
      .get('.validation-list > .error').first().contains(
        'Email is required.');
  });

  it('should allow a user to log in', () => {
    cy
      .visit('/register')
      .get('input[name="username"]').type(username)
      .get('input[name="email"]').type(email)
      .get('input[name="password"]').type(password)
      .get('input[type="submit"]').click();

    cy.get('.navbar-burger').click();
    cy.contains('Log Out').click();

    cy
      .get('a').contains('Log In').click()
      .get('input[name="email"]').type(email)
      .get('input[name="password"]').type(password)
      .get('input[type="submit"]').click()
      .wait(100);

    cy.contains('All Users');
    cy
      .get('table')
      .get('tbody > tr').last()
      .find('td').contains(username);
    cy.get('.notification.is-success').contains('Welcome!');
    cy.get('.navbar-burger').click();
    cy.get('.navbar-menu').within(() => {
      cy
        .get('.navbar-item').contains('User Status')
        .get('.navbar-item').contains('Log Out')
        .get('.navbar-item').contains('Log In').should('not.be.visible')
        .get('.navbar-item').contains('Register').should('not.be.visible');
    });
  });

  it('should throw an error if the credentials are incorrect', () => {
    cy
      .visit('/login')
      .get('input[name="email"]').type('incorrect@email.com')
      .get('input[name="password"]').type(password)
      .get('input[type="submit"]').click();

    cy.contains('All Users').should('not.be.visible');
    cy.contains('Log In');

    cy.get('.navbar-burger').click();
    cy.get('.navbar-menu').within(() => {
      cy
        .get('.navbar-item').contains('User Status').should('not.be.visible')
        .get('.navbar-item').contains('Log Out').should('not.be.visible')
        .get('.navbar-item').contains('Log In')
        .get('.navbar-item').contains('Register');
    });
    cy
      .get('.notification.is-success').should('not.be.visible')
      .get('.notification.is-danger').contains('User does not exist.');

    cy
      .get('a').contains('Log In').click()
      .get('input[name="email"]').type(email)
      .get('input[name="password"]').type('incorrectpassword')
      .get('input[type="submit"]').click()
      .wait(100);

    cy.contains('All Users').should('not.be.visible');
    cy.contains('Log In');

    cy.get('.navbar-burger').click();
    cy.get('.navbar-menu').within(() => {
      cy
        .get('.navbar-item').contains('User Status').should('not.be.visible')
        .get('.navbar-item').contains('Log Out').should('not.be.visible')
        .get('.navbar-item').contains('Log In')
        .get('.navbar-item').contains('Register');
    });
  })
})