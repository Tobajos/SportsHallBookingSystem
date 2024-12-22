describe('Login Page', () => {
    beforeEach(() => {
      cy.visit('/login');
    });
  
    it('should display the login form', () => {
      cy.get('form').should('be.visible');
      cy.get('input[name="email"]').should('be.visible').and('have.attr', 'placeholder', 'Email');
      cy.get('input[name="password"]').should('be.visible').and('have.attr', 'placeholder', 'Password');
      cy.get('button[type="submit"]').contains('Login').should('be.visible');
    });
  
    it('should log in successfully with valid credentials', () => {

      cy.intercept('POST', '/auth/login/', {
        statusCode: 200,
        body: {
          message: 'Logged in successfully!',
          user_id: 1,
          firstname: 'John',
          lastname: 'Doe',
          email: 'validuser@example.com',
        },
      }).as('loginRequest');

      cy.get('input[name="email"]').type('validuser@example.com');
      cy.get('input[name="password"]').type('correctpassword');
      cy.get('button[type="submit"]').click();

      cy.wait('@loginRequest').its('request.body').should('deep.equal', {
        email: 'validuser@example.com',
        password: 'correctpassword',
      });

      cy.get('.error-message').should('not.exist'); 
      cy.url().should('include', '/'); 
    });
  
    it('should show an error message with invalid credentials', () => {
      cy.intercept('POST', '/auth/login/', {
        statusCode: 400,
        body: { message: 'Invalid credentials. Please try again.' },
      }).as('loginRequest');
  
      cy.get('input[name="email"]').type('invaliduser@example.com');
      cy.get('input[name="password"]').type('wrongpassword');
      cy.get('button[type="submit"]').click();
  
      cy.wait('@loginRequest').its('request.body').should('deep.equal', {
        email: 'invaliduser@example.com',
        password: 'wrongpassword',
      });
  
      cy.get('.error-message')
        .should('be.visible')
        .and('contain', 'Invalid credentials. Please try again.');
    });
  
    it('should navigate to the registration page', () => {
      cy.get('a').contains('Sign up here').click();
      cy.url().should('include', '/register');
    });
  });
  