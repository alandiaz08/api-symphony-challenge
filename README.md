# API Symphony Challenge

This project contains automated tests to verify the functionality of an API based on Django Rest Framework. The tests include user registration, login, creating posts, adding comments, and reading comments.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/api-symphony-challenge.git
   cd api-symphony-challenge

2. Create and activate a virtual environment:
   ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. Install dependencies:
   ```bash
    pip install -r requirements.txt

## Usage

### Configuration

1. Update the config.py file with the base URL of the API
    ```bash
   BASE_URL = "https://randomlyapi.symphony.is/api"

### Running Tests
    ```bash
    pytest tests/

## Project Structure
- tests/test_api.py: Contains all the tests for the API endpoints.
- config.py: Contains the configuration for the base URL of the API.

## Tested Endpoints
1. POST /api/auth/signup/: Registers a new user.
2. POST /api/auth/login/: Logs in and obtains the authorization token.
3. POST /api/posts/: Creates a new post.
4. POST /api/post-comments/: Adds a comment to a post.
5. GET /api/posts/{id}/comments/: Retrieves comments for a post.
