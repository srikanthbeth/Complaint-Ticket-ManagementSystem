def get_token(client):

    response = client.post(
        "/auth/login",
        json={
            "email": "admin@gmail.com",
            "password": "admin123"
        }
    )

    return response.json()["access_token"]


def test_create_customer(test_client):

    token = get_token(test_client)

    response = test_client.post(
        "/customers/",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "name": "John",
            "email": "john@gmail.com",
            "phone": "9876543210",
            "address": "Hyderabad"
        }
    )

    assert response.status_code in [200, 201, 400]


def test_get_customers(test_client):

    token = get_token(test_client)

    response = test_client.get(
        "/customers/",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200