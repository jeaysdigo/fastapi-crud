# User Management REST API

## Description

This is a simple User Management REST API built with FastAPI that supports user registration, authentication, and profile management.

## Installation

1. Clone the repository.
   ```bash
   https://github.com/jeaysdigo/fastapi-crud.git
   ```
2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file.
4. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```

## Endpoints

- **POST** `/register`: Register a new user.
- **POST** `/login`: Login and receive JWT.
- **GET** `/users/{user_id}`: Retrieve a user profile.
- **PUT** `/users/{user_id}`: Update a user profile.
- **DELETE** `/users/{user_id}`: Delete a user profile.

API Specs: http://127.0.0.1:8000/docs
