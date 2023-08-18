# Users module

---

## API Endpoints

***Available without authorization***
- /users/register (POST)
    - Register new user by email and password
- /users/login/ (POST)
    - Complete fist step of authorization with email address and password
    - After success sends an email with OTP
- /users/confirm-otp/ (POST)
    - Complete second step of authorization with OTP from received email

***Requires authorization***
- /users/{id}/ (GET)
    - Fetch user profile by his id, no specific access restrictions
- /users/{id}/ (DELETE)
    - Delete user account by his id, can be done only by user himself or superuser
- /users/{id}/ (PATCH)
  - Update user profile by his id, can be done only by user himself or staff
