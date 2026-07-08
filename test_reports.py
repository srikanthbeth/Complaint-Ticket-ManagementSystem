def get_token(client):

    response = client.post(
        "/auth/login",
        json={
            "email": "admin@gmail.com",
            "password": "admin123"
        }
    )

    return response.json()["access_token"]


def test_search_tickets(test_client):

    token = get_token(test_client)

    response = test_client.get(
        "/reports/tickets?title=Internet",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200


def test_filter_priority(test_client):

    token = get_token(test_client)

    response = test_client.get(
        "/reports/tickets?priority=High",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200


def test_filter_status(test_client):

    token = get_token(test_client)

    response = test_client.get(
        "/reports/tickets?status=Open",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200


def test_customer_tickets(test_client):

    token = get_token(test_client)

    response = test_client.get(
        "/reports/customers/1/tickets",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200