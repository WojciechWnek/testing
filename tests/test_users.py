import pytest


def test_user_registration(client):
    response = client.post(
        "/register", json={"email": "boris@example.com", "password": "secret123"}
    )

    assert response.status_code == 201
    assert response.json()["email"] == "boris@example.com"


def test_user_login(client, user):
    login_response = client.post(
        "/token", data={"username": user.email, "password": "secret123"}
    )
    assert login_response.status_code == 200

    data = login_response.json()
    assert "access_token" in data


def test_user_login_with_wrong_password(client, user):
    login_response = client.post(
        "/token", data={"username": user.email, "password": "wrongpassword"}
    )
    assert login_response.status_code == 401


@pytest.mark.usefixtures("user")
def test_user_login_with_nonexistent_email(client):
    login_response = client.post(
        "/token", data={"username": "nobody@example.com", "password": "wrongpassword"}
    )
    assert login_response.status_code == 401


@pytest.mark.usefixtures("user")
def test_users_me_without_a_token(client):
    response = client.get("/users/me")
    assert response.status_code == 401


@pytest.mark.usefixtures("user")
def test_users_me_with_an_invalid_token(client):
    response = client.get(
        "/users/me", headers={"Authorization": "Bearer nobody@example.com"}
    )
    assert response.status_code == 401


def test_users_me_with_a_valid_token(client, user):
    response = client.get(
        "/users/me", headers={"Authorization": f"Bearer {user.email}"}
    )
    assert response.status_code == 200
    assert response.json()["email"] == user.email
