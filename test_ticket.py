def get_token(client):

    response = client.post(
        "/auth/login",
        json={
            "email": "admin@gmail.com",
            "password": "admin123"
        }
    )

    return response.json()["access_token"]


def test_create_ticket(test_client):

    token = get_token(test_client)

    response = test_client.post(
        "/tickets/",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "customer_id": 1,
            "title": "Internet Issue",
            "description": "No internet",
            "priority": "High",
            "category": "Network"
        }
    )

    assert response.status_code in [200, 201, 404]


def test_get_tickets(test_client):

    token = get_token(test_client)

    response = test_client.get(
        "/tickets/",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200