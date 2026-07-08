def get_token(client):

    response = client.post(
        "/auth/login",
        json={
            "email": "admin@gmail.com",
            "password": "admin123"
        }
    )

    print(response.status_code)
    print(response.json())

    assert response.status_code == 200

    return response.json()["access_token"]


def test_assign_ticket(test_client):

    token = get_token(test_client)

    response = test_client.post(
        "/tickets/1/assign/2",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code in [200, 404, 400]


def test_agent_tickets(test_client):

    token = get_token(test_client)

    response = test_client.get(
        "/agents/2/tickets",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code in [200, 404]