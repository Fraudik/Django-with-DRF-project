# Django-with-DRF-project
Webshop based on Django and DRF. Includes products, users with OTP confirmation on email and chats with websockets. 

This project uses the following technologies for development, setup and deployment:
- [ ]  Docker for containerization.
- [ ]  Poetry for version control.
- [ ]  Gunicorn as web server.
WhiteNoise helps in serving static files.

Also using OpenAPI 3.0 schema with library drf-spectacular. Swagger located at URL "/docs/swagger/".

---

## Environment settings
.env:
- DEBUG
  - 0 or 1 as False or True for debug purposes
- SECRET_KEY
  - Secret key used by Django
- WEB_PORT
  -  The port on which the site is located
- SQL_DATABASE. SQL_USER, SQL_PASSWORD
  - Database configuration settings, must match the corresponding settings in .env.db.
- SQL_HOST, SQL_PORT
  - Database container name
- EMAIL_HOST, EMAIL_PORT, EMAIL_USE_TLS, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD
  - Settings for sending emails from SMTP server

The PostgreSQL database was selected by default.

---

## Users module

### Stack

Except Django and DRF also used:
- [ ] PyOTP
- [ ] Celery
- [ ] Redis

As password hasher used Argon2, configured validators for password.

### API Endpoints

***Available without authorization***
- /users/register (POST)
    - Register new user by email and password
- /users/login/ (POST)
    - Complete fist step of authorization with email address and password
    - After success sends an email with OTP
- /users/confirm-otp/ (POST)
    - Complete second step of authorization with OTP from received email

***Require authorization***
- /users/{id}/ (GET)
    - Fetch user profile by his id, no specific access restrictions
- /users/{id}/ (DELETE)
    - Delete user account by his id, can be done only by user himself or superuser
- /users/{id}/ (PATCH)
  - Update user profile by his id, can be done only by user himself or staff
 
---

## Products module

### API Endpoints

***Available without authorization***
- /api/v2/products/ (GET)
    - List all existing products
- /api/v2/products/{title}/
  - Get product by title
- /search/
  - Search products by title or part of it

***Require authorization***
  - /products/ (GET)
    - List all existing products
  - /products/ (POST)
    - Create new product
  - /products/{title}/ (GET)
      - Get product by title
  - /products/{title}/update/ (PUT)
      - Update product info by title
  - /products/{title}/delete/ (DELETE)
      - Delete product by title

## Chats module


### Stack

Except Django and DRF also used:
- [ ] Django Channels
- [ ] Daphne
- [ ] Redis
Has templates, .js and .css files for better showcase.

Chats work on websockets. All events in them are logged.

### API Endpoints

***Require authorization***
- /chat/
  - Access index page with field for chat name (new or existing one)
- /chat/{chatName}
   - Enter chat by name
   - Allows to send and receive messages in chat with this name

