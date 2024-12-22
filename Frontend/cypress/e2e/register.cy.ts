describe('Registration Page', () => {
    beforeEach(() => {
      cy.visit('/register');
    });
  
    it('should display the registration form', () => {
      // Sprawdź, czy formularz rejestracji jest widoczny
      cy.get('form').should('be.visible');
      cy.get('input[name="email"]').should('be.visible').and('have.attr', 'placeholder', 'email');
      cy.get('input[name="password"]').should('be.visible').and('have.attr', 'placeholder', 'password');
      cy.get('input[name="firstname"]').should('be.visible').and('have.attr', 'placeholder', 'firstname');
      cy.get('input[name="lastname"]').should('be.visible').and('have.attr', 'placeholder', 'lastname');
      cy.get('button').contains('Sign up').should('be.visible');
    });
  
    it('should show an error for invalid email format', () => {
      cy.get('input[name="email"]').type('invalidemail');
      cy.get('input[name="password"]').type('password123');
      cy.get('input[name="firstname"]').type('John');
      cy.get('input[name="lastname"]').type('Doe');
      cy.get('button').contains('Sign up').click();
  

      cy.get('.error-message').should('be.visible').and('contain', 'Registration failed. Please try again');
    });
  
    it('should successfully register with valid inputs', () => {
      cy.intercept('POST', '/auth/register/', {
        statusCode: 201,
        body: { message: 'Account created successfully!' },
      }).as('registerRequest');
  
      cy.get('input[name="email"]').type('newuser@example.com');
      cy.get('input[name="password"]').type('password123');
      cy.get('input[name="firstname"]').type('John');
      cy.get('input[name="lastname"]').type('Doe');
      cy.get('button').contains('Sign up').click();
  
      cy.wait('@registerRequest').its('request.body').should('deep.equal', {
        email: 'newuser@example.com',
        password: 'password123',
        firstname: 'John',
        lastname: 'Doe',
      });
  
      // Sprawdź, czy pojawia się komunikat sukcesu
      cy.get('.success-message').should('be.visible').and('contain', 'Account created successfully!');
  
      // Sprawdź, czy użytkownik został przekierowany na stronę logowania
      cy.url().should('include', '/login');
    });
  
    it('should show an error message for duplicate email', () => {
      // Mockowanie odpowiedzi API dla istniejącego emaila
      cy.intercept('POST', '/auth/register/', {
        statusCode: 400,
        body: { errors: ['email: This email is already registered.'] },
      }).as('registerRequest');
  
      // Wprowadź dane z duplikatem emaila
      cy.get('input[name="email"]').type('tobiasz.podlesny@gmail.com');
      cy.get('input[name="password"]').type('password123');
      cy.get('input[name="firstname"]').type('John');
      cy.get('input[name="lastname"]').type('Doe');
      cy.get('button').contains('Sign up').click();
  
      // Sprawdź, czy pojawia się odpowiedni komunikat o błędzie
      cy.get('.error-message').should('be.visible').and('contain', 'email: This email is already registered.');
    });
  });
  