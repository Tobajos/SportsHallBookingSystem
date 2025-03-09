# SportsHallBookingSystem

## Description
This project is a modern web application designed for booking a sports hall for basketball games. The system allows users to check availability, make reservations, organize tournaments, and join open matches. Additionally, users can post announcements to find players for games. The application includes an interactive calendar and user management features, ensuring an efficient and smooth booking process.

## Features
- Interactive calendar for hall reservations
- Open and closed reservations
- Tournament and match organization
- User profiles with reservation management
- Announcement board for finding players
- Administrator panel for managing users and bookings
- End-to-end testing with Cypress
- Backend integration testing

## Technology Stack
- **Frontend**: Angular  
- **Backend**: Django REST Framework (Python)  
- **Database**: PostgreSQL  
- **Version Control**: Git & GitHub  
- **Testing**:  
  - Cypress for end-to-end testing  
  - Django test framework for backend integration testing  

## Installation and Configuration Guide

### 1. Backend Configuration
Follow these steps to set up and run the backend using Django:

1. Navigate to the backend directory:
   ```sh
   cd backend
   ```
2. Create a virtual environment:
   ```sh
   python -m venv env_name
   ```
3. Activate the virtual environment:
   - On Windows:
     ```sh
     .\env_name\Scripts\activate
     ```
   - On macOS/Linux:
     ```sh
     source env_name/bin/activate
     ```
4. Install dependencies from `requirements.txt`:
   ```sh
   pip install -r requirements.txt
   ```
5. Configure the database by editing `settings.py` in the backend directory:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'your_database_name',
           'USER': 'your_username',
           'PASSWORD': 'your_password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```
   If PostgreSQL is not used, the default database is SQLite.
6. Apply database migrations:
   ```sh
   python manage.py makemigrations
   python manage.py migrate
   ```
7. Run the backend server:
   ```sh
   python manage.py runserver
   ```

### 2. Frontend Configuration
Follow these steps to set up and run the frontend using Angular:

8. Navigate to the frontend directory:
   ```sh
   cd frontend
   ```
9. Install Angular dependencies:
   ```sh
   npm install -f
   ```
10. Run the frontend server:
    ```sh
    ng serve
    ```

### 3. Accessing the Application
After successfully running both backend and frontend, open your browser and navigate to:

**[http://localhost:4200](http://localhost:4200)**

Now, you can start using the sports hall booking system.

## Testing
- **End-to-end tests**: The application includes Cypress-based E2E tests to verify UI workflows.
- **Backend integration tests**: Django's built-in testing framework is used to validate API and business logic functionality.

###Calendar Page
![obraz](https://github.com/user-attachments/assets/750c3f78-1431-4343-8390-5120daba91ec)


###Sign up Page
![obraz](https://github.com/user-attachments/assets/72a32e4d-8722-43bf-ab7a-1561a1612b82)


###Login Page
![obraz](https://github.com/user-attachments/assets/2b4398d7-7011-43df-8f44-1dd79cf7c31e)



