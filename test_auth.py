def test_register(test_client):

    response = test_client.post(
        "/auth/register",
        json={
            "name": "Admin",
            "email": "admin@gmail.com",
            "password": "admin123",
            "role": "Admin"
        }
    )

    assert response.status_code in [200, 201, 400]


def test_login(test_client):

    response = test_client.post(
        "/auth/login",
        json={
            "email": "admin@gmail.com",
            "password": "admin123"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data