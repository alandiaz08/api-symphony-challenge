import requests
import pytest
from config import BASE_URL


@pytest.fixture(scope="module")
def user_data():
    return {
        "email": "testuser@example.com",
        "password": "testpassword123",
        "firstName": "Test",
        "lastName": "User",
        "username": "testuser",
        "dateOfBirth": "1990-01-01"
    }


@pytest.fixture(scope="module")
def headers():
    return {
        "Content-Type": "application/json"
    }


@pytest.fixture(scope="module")
def token(user_data, headers):
    # Register a new user
    signup_response = requests.post(f"{BASE_URL}/auth/signup", json=user_data, headers=headers)
    print("Signup response status code:", signup_response.status_code)
    print("Signup response text:", signup_response.text)
    print("Signup response headers:", signup_response.headers)
    print("Signup request payload:", user_data)
    print("Signup request headers:", headers)

    if signup_response.status_code != 201:
        pytest.fail(f"Signup failed: {signup_response.status_code} - {signup_response.text}")

    # Login to get the token
    login_data = {
        "username": user_data["username"],
        "password": user_data["password"]
    }
    login_response = requests.post(f"{BASE_URL}/auth/login", json=login_data, headers=headers)
    print("Login response status code:", login_response.status_code)
    print("Login response text:", login_response.text)
    print("Login response headers:", login_response.headers)

    if login_response.status_code != 200:
        pytest.fail(f"Login failed: {login_response.status_code} - {login_response.text}")

    return login_response.json()["token"]


@pytest.fixture(scope="module")
def auth_headers(token):
    return {
        "Authorization": f"token {token}",
        "Content-Type": "application/json"
    }


@pytest.fixture(scope="module")
def post_data(auth_headers):
    post_payload = {
        "text": "This is a test post"
    }
    post_response = requests.post(f"{BASE_URL}/posts", json=post_payload, headers=auth_headers)
    print("Post response status code:", post_response.status_code)
    print("Post response text:", post_response.text)
    print("Post response headers:", post_response.headers)

    if post_response.status_code != 201:
        pytest.fail(f"Post creation failed: {post_response.status_code} - {post_response.text}")

    return post_response.json()


def test_signup(user_data, headers):
    response = requests.post(f"{BASE_URL}/auth/signup", json=user_data, headers=headers)
    print("Signup response status code:", response.status_code)
    print("Signup response text:", response.text)
    print("Signup response headers:", response.headers)
    print("Signup request payload:", user_data)
    print("Signup request headers:", headers)

    assert response.status_code == 201
    assert "id" in response.json()
    assert "username" in response.json()
    assert response.json()["username"] == user_data["username"]


def test_login(user_data, headers):
    login_data = {
        "username": user_data["username"],
        "password": user_data["password"]
    }
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data, headers=headers)
    print("Login response status code:", response.status_code)
    print("Login response text:", response.text)
    print("Login response headers:", response.headers)

    assert response.status_code == 200
    assert "token" in response.json()


def test_create_post(auth_headers):
    post_payload = {
        "text": "This is a test post"
    }
    response = requests.post(f"{BASE_URL}/posts", json=post_payload, headers=auth_headers)
    print("Create post response status code:", response.status_code)
    print("Create post response text:", response.text)
    print("Create post response headers:", response.headers)

    assert response.status_code == 201
    assert "id" in response.json()
    assert response.json()["text"] == post_payload["text"]


def test_add_comment(auth_headers, post_data):
    comment_payload = {
        "post": post_data["id"],
        "text": "This is a test comment"
    }
    response = requests.post(f"{BASE_URL}/post-comments", json=comment_payload, headers=auth_headers)
    print("Add comment response status code:", response.status_code)
    print("Add comment response text:", response.text)
    print("Add comment response headers:", response.headers)

    assert response.status_code == 201
    assert "id" in response.json()
    assert response.json()["text"] == comment_payload["text"]


def test_read_comments(auth_headers, post_data):
    response = requests.get(f"{BASE_URL}/posts/{post_data['id']}/comments", headers=auth_headers)
    print("Read comments response status code:", response.status_code)
    print("Read comments response text:", response.text)
    print("Read comments response headers:", response.headers)

    assert response.status_code == 200
    comments = response.json()
    assert isinstance(comments, list)
    assert len(comments) > 0
    assert comments[0]["text"] == "This is a test comment"

